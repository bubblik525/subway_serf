from pathlib import Path
import argparse, hashlib, json, xml.etree.ElementTree as ET
import cv2
import numpy as np
ROOT = Path(__file__).resolve().parents[1]

def verify(root=ROOT):
    manifest = json.loads((root / 'data/manifest.json').read_text())
    for item in manifest['files']:
        p = root / item['path']
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError(f'Asset integrity check failed: {p}')
    return manifest

def graph(path):
    ns = {'g': 'http://graphml.graphdrawing.org/xmlns'}
    g = ET.parse(path).getroot().find('g:graph', ns)
    if g.attrib['edgedefault'] != 'directed':
        raise ValueError('Expected directed graph')
    ids = [n.attrib['id'] for n in g.findall('g:node', ns)]
    index = {k: i for i, k in enumerate(ids)}
    a = np.zeros((len(ids), len(ids)), dtype=np.float32)
    for e in g.findall('g:edge', ns):
        a[index[e.attrib['target']], index[e.attrib['source']]] = 1
    return ids, a

def features(rgb, previous=None):
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError('Expected H x W x 3 RGB pixels')
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    small = cv2.resize(gray, (8, 8), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    change = 0.0 if previous is None else float(np.abs(small - previous).mean())
    return np.r_[small.ravel(), change].astype(np.float32), small

class AreaReservoir:
    """Engineered rate dynamics; graph nodes are areas, not individual neurons."""
    def __init__(self, adjacency, seed=7):
        n = len(adjacency)
        self.weights = adjacency / np.maximum(adjacency.sum(axis=1, keepdims=True), 1)
        self.input = np.random.default_rng(seed).normal(0, .12, (n, 65)).astype(np.float32)
        self.state = np.zeros(n, dtype=np.float32)
    def step(self, sensory):
        if sensory.shape != (65,) or not np.isfinite(sensory).all():
            raise ValueError('Expected 65 finite image features')
        self.state = (.8*self.state + .2*np.tanh(.65*self.weights@self.state + self.input@sensory)).astype(np.float32)
        return self.state.copy()

def replay(video, output, frames=150):
    verify()
    ids, a = graph(ROOT / 'data/cat-cortex.graphml')
    model = AreaReservoir(a)
    cap = cv2.VideoCapture(str(video))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not cap.isOpened() or fps <= 0:
        raise ValueError('Video cannot be opened')
    output.mkdir(parents=True, exist_ok=True)
    previous = None
    count = 0
    with (output / 'observations.jsonl').open('w') as log:
        for i in range(frames):
            ok, frame = cap.read()
            if not ok: break
            sensory, previous = features(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), previous)
            state = model.step(sensory)
            log.write(json.dumps({'frame':i, 'time_s':i/fps, 'mean_luminance':float(sensory[:64].mean()), 'frame_change':float(sensory[-1]), 'area_state':state.tolist(), 'action':None})+'\n')
            count += 1
    cap.release()
    if not count: raise ValueError('No decoded frames')
    np.savez_compressed(output/'checkpoint.npz', state=model.state, previous=previous, seed=7, frames=count)
    return {'frames':count, 'areas':len(ids), 'edges':int(a.sum()), 'mode':'offline; no trained policy; no game input'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('command', choices=['prepare','verify','replay'])
    p.add_argument('--video', type=Path, default=ROOT/'data/gameplay-sample.mp4')
    p.add_argument('--out', type=Path, default=ROOT/'runs/replay')
    p.add_argument('--frames', type=int, default=150)
    args=p.parse_args()
    if args.frames < 1: p.error('--frames must be positive')
    if args.command in ('prepare','verify'):
        m=verify(); ids,a=graph(ROOT/'data/cat-cortex.graphml')
        print(json.dumps({'verified_files':len(m['files']), 'areas':len(ids), 'edges':int(a.sum())}))
    else: print(json.dumps(replay(args.video,args.out,args.frames)))
if __name__ == '__main__': main()
