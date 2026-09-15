"""Training entry point reserved for supervised imitation learning.

Planned input: synchronized episode/frame/action records with area-state histories.
The current replay fixture has no action labels and cannot train this controller.
"""
import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TrainingConfig:
    dataset: Path
    output: Path = Path('runs/controller')
    seed: int = 7
    history_frames: int = 8
    learning_rate: float = 0.001
    epochs: int = 30
    batch_size: int = 64


def train(config: TrainingConfig) -> None:
    if not config.dataset.is_file():
        raise FileNotFoundError(f'Labeled episode manifest not found: {config.dataset}')
    # TODO: validate episode_id, frame, time_s, action and area_state records.
    # TODO: form causal history windows without crossing episode boundaries.
    # TODO: split whole episodes into train/validation/evaluation partitions.
    # TODO: fit a temporal readout using action cross-entropy and fixed seeds.
    # TODO: save weights, action order, config, dataset hashes and held-out metrics.
    # TODO: verify loading the checkpoint through Controller.predict before release.
    raise NotImplementedError('Training is scaffolded; dataset loading and optimization are pending.')


def main() -> None:
    parser = argparse.ArgumentParser(description='Controller training scaffold; optimization is not implemented yet.')
    parser.add_argument('--dataset', type=Path, required=True, help='Future labeled episode manifest')
    parser.add_argument('--out', type=Path, default=Path('runs/controller'))
    parser.add_argument('--seed', type=int, default=7)
    args = parser.parse_args()
    try:
        train(TrainingConfig(dataset=args.dataset, output=args.out, seed=args.seed))
    except (FileNotFoundError, NotImplementedError) as exc:
        parser.exit(2, f'{exc}\n')


if __name__ == '__main__':
    main()
