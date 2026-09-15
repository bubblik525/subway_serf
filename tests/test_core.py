import tempfile, unittest
from pathlib import Path
import numpy as np
from catbrain.__main__ import ROOT, AreaReservoir, features, graph, verify, replay

class CoreTests(unittest.TestCase):
    def test_asset_integrity(self):
        self.assertGreaterEqual(len(verify()['files']), 5)
    def test_graph_contract(self):
        ids,a=graph(ROOT/'data/cat-cortex.graphml')
        self.assertEqual((len(ids),int(a.sum())),(65,1139))
        self.assertFalse(np.array_equal(a,a.T))
    def test_sensory_response(self):
        dark,prev=features(np.zeros((64,64,3),np.uint8))
        light,_=features(np.full((64,64,3),255,np.uint8),prev)
        self.assertEqual(float(dark.sum()),0)
        self.assertEqual(float(light[-1]),1)
    def test_determinism_and_input_path(self):
        _,a=graph(ROOT/'data/cat-cortex.graphml')
        m,n=AreaReservoir(a),AreaReservoir(a)
        np.testing.assert_array_equal(m.step(np.ones(65)),n.step(np.ones(65)))
        self.assertGreater(float(np.linalg.norm(m.state)),0)
    def test_state_bounded_and_invalid_input(self):
        _,a=graph(ROOT/'data/cat-cortex.graphml');m=AreaReservoir(a)
        for _ in range(100):m.step(np.full(65,100))
        self.assertTrue(np.all(np.abs(m.state)<=1))
        with self.assertRaises(ValueError):m.step(np.full(65,np.nan))
    def test_video_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);r=replay(ROOT/'data/gameplay-sample.mp4',p,8)
            self.assertEqual(r['frames'],8)
            self.assertEqual(len((p/'observations.jsonl').read_text().splitlines()),8)
            with np.load(p/'checkpoint.npz') as state:
                self.assertEqual(state['state'].shape,(65,))
if __name__=='__main__': unittest.main()
