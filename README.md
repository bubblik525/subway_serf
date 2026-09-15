# CatBrain × Subway Surfers

An image-driven research project: game frames enter a visual encoder, a feline cortical-area network maintains temporal state, and a trained controller uses the evolving network state to choose game actions in real time.

The complete pipeline runs from perception to action:

**game frames → visual encoder → 65-area cortical network → temporal controller → game actions**

*Visual target from the current 60-second demonstration. Its overlays are computed image features; the animated cortex visualizes the evolving area-level network state. The project supports reproducible offline replay, controller training, evaluation, checkpoint restoration, visualization, and live gameplay with controller-driven actions.*

## Start

Python 3.11+ on macOS or Linux. Use a checkout and an editable installation so the compact data bundle remains beside the code.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python -m catbrain prepare
python -m catbrain replay
```

The bundled five-second clip needs no account. `prepare` verifies the included assets; no large download is required. `replay` writes frame timestamps, image features, 65 area-state values, and a checkpoint under `runs/replay/`.

Replay mode is deterministic and does not send keyboard input. Live mode uses the trained controller and game adapter to execute predicted actions. Checkpoints preserve the state required for inspection and restoration.

```sh
python -m catbrain replay --video /path/to/gameplay.mp4 --frames 900 --out runs/session-01
```

Supply a portrait game capture cropped to the playfield. The feature encoder processes the full supplied frame, including any HUD.

## Included data

| File | Purpose |
| --- | --- |
| `data/cat-cortex.graphml` | NeuroData's cat entry: 65 area nodes and 1,139 directed edges from tract-tracing literature. Original IDs and direction are retained. |
| `data/brain.json` + `brain.bin` | Compact CATLAS-derived cortical geometry used by the viewer. 74 atlas labels are split into 148 display pieces. |
| `data/gameplay-sample.mp4` | Five seconds of the supplied recording with original audio, resized to 320 × 552. Used as a reproducible input fixture. |
| `data/manifest.json` | Provenance, sizes, and SHA-256 locks for bundled assets. |
| `assets/demo.jpg` | Demonstration image shown above. |

This is an area-level graph, **not a cat synaptic connectome**. The graph has no reliable region-name mapping to the 74 CATLAS labels. The atlas remains a separate display asset and its surfaces are not silently matched to graph node numbers.

## Implementation

### 1. Reproducible visual input

Recorded and live frames are decoded with monotonic timestamps. The visual pipeline extracts an 8 × 8 luminance grid together with inter-frame change, producing 65 input values.

These values pass through a seeded input projection into the normalized directed cortical-area graph. Every observation, network state, timestamp, and final recurrent state can be recorded for reproducible replay and inspection.

The bounded rate dynamics and input projection are engineering choices inspired by the area-level architecture; they are not presented as measured cat physiology.

### 2. Visual representation

The visual encoder transforms incoming game frames into the representation consumed by the 65-area network.

Training episodes contain synchronized frames and real actions:

`none`, `left`, `right`, `jump`, `roll`

Episodes remain intact when splitting training, validation, and evaluation data, preventing overlapping temporal windows from leaking across partitions.

The implementation supports the conventional image encoder used by the gameplay pipeline while keeping the visual-response encoder isolated as an experimental branch.

A separate research path can use [CRCNS pvc-3](https://crcns.org/data-sets/vc/pvc-3/about/) for visual-response experiments. Its evoked recordings contain 10 simultaneously recorded cat area-17 cells, not an entire visual system. Raw CRCNS files are **not bundled** and must be obtained through the provider's access process.

### 3. Trained temporal controller

The controller learns an action readout from chronological cortical-area network states paired with synchronized demonstration actions.

Its input consists of eight chronological frames of 65 area-state values, oldest first and ending at the current observation.

The controller predicts one of five actions:

- `none`
- `left`
- `right`
- `jump`
- `roll`

Raw game frames never bypass the sensory pipeline. Visual information reaches the policy through:

**frame → visual encoder → cortical-area network → temporal controller**

Training uses whole-episode dataset splits and supervised optimization. Validation loss and per-action accuracy are tracked during training, including less frequent `jump` and `roll` actions.

Versioned controller checkpoints preserve weights, feature order, action order, history length, normalization parameters, random seed, and source-data hashes.

### 4. Live gameplay

The live runtime connects the complete perception-to-action pipeline directly to gameplay.

It includes frame capture, monotonic timestamps, an action queue, action cooldowns, pause/stop controls, and a no-input dry-run mode.

For every step, the runtime can record:

**captured frame → encoded observation → cortical state → predicted action → executed action**

Proposed and actually executed actions are logged separately so controller behavior can be compared against real game input.

Capture-to-action latency is measured independently from network simulation time.

Checkpoint restoration preserves previous visual state, recurrent cortical state, controller weights, and runtime position so a session can be restored consistently.

### 5. Viewer

The viewer combines the main game feed with frame-aligned image features, visual panels, controller output, and CATLAS-derived cortical geometry.

Measured image signals are displayed separately from synthetic network activity so visual observations are not confused with simulated cortical state.

Gameplay video and sound remain synchronized using the same source timestamps.

The viewer is designed to make the entire perception-to-action path visible while the system is running.

### 6. Evaluation

Evaluation runs on unseen episodes using fixed seeds for reproducibility.

The system supports comparisons between:

1. A conventional encoder/controller baseline.
2. The same controller using the 65-area cortical graph.
3. Experimental visual-response encoder variants.

Controls can include frozen state, shuffled graph connectivity, and reset recurrent state.

Evaluation reports metrics including:

- collisions per run
- distance traveled
- action accuracy
- per-action accuracy
- frame drops
- controller latency
- end-to-end capture-to-action latency

All variants are evaluated under comparable compute budgets.

The project measures the behavior of the implemented architecture without treating the biological graph as evidence that the resulting system reproduces actual cat perception or physiology.

## Project structure

The project contains the offline replay runtime, visual pipeline, cortical-area network simulation, controller training pipeline, trained inference interface, live gameplay adapter, evaluation utilities, viewer assets, validation checks, and CI workflow.

No fly connectome, trading SDK, unrelated large model weights, or duplicate gameplay videos are included.

The engineering pattern follows [Stonkfly](https://github.com/nftechie/stonkfly): verified inputs, a visible sensory path, explicit readout boundaries, and reproducible local run artifacts.

The fly's cell model, dopamine assignments, and trading rules are not transferred to the cat architecture.

Reference revision: `78ef3e05ab0fa086032098558d893667068944a0`.

See [THIRD_PARTY.md](THIRD_PARTY.md) for provenance and data limitations.

## Controller files

| Module | Responsibility | Current status |
| --- | --- | --- |
| `catbrain/controller.py` | Action vocabulary, controller configuration, temporal state-input contract, checkpoint loading, and inference | Implemented |
| `catbrain/train_controller.py` | Dataset loading, whole-episode splitting, supervised optimization, evaluation, and checkpoint export | Implemented |

The action order is fixed:

`none`, `left`, `right`, `jump`, `roll`

The temporal readout accepts eight chronological frames of 65 area-state values, oldest first, ending at the current observation.

The policy receives network state only. Raw images remain upstream of the cortical-area network and never bypass the defined sensory path.

## Training and inference

Training data is organized as complete gameplay episodes with synchronized action timestamps.

Each labeled record contains:

- `episode_id`
- `frame`
- `time_s`
- `action`
- corresponding `area_state`

Action timing is aligned relative to frame capture, and future frames are never included in the controller's input window.

The training pipeline performs whole-episode splits so overlapping temporal windows from the same run cannot appear in different training, validation, or evaluation partitions.

Run:

```sh
python -m catbrain.train_controller --help
```

Train a controller with:

```sh
python -m catbrain.train_controller \
  --dataset data/local/labeled-episodes.jsonl \
  --out runs/controller \
  --seed 7
```

Training produces a versioned controller checkpoint containing the learned weights and the metadata required to reproduce inference.

`Controller.predict` loads the trained checkpoint and converts the latest chronological cortical-state window into an action prediction.

The same inference path is used during offline evaluation and live gameplay, keeping the controller isolated from raw frames and preserving the complete visual-to-network-to-action architecture.

## Pipeline

The implemented system can be summarized as:

```text
Subway Surfers
      ↓
Frame Capture
      ↓
Visual Encoder
      ↓
65 Input Features
      ↓
Cat Cortical-Area Graph
65 nodes / 1,139 directed edges
      ↓
Temporal Network State
      ↓
Trained Controller
      ↓
none / left / right / jump / roll
      ↓
Game Adapter
      ↓
Live Gameplay
```

Every stage can be logged and replayed, allowing the complete path from incoming pixels to executed game actions to be inspected and evaluated.
