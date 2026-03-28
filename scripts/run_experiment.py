from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = REPO_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from quantum_healthcare_optimizer.config import ExperimentConfig
from quantum_healthcare_optimizer.experiment import run_experiment, save_experiment


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the quantum healthcare optimizer experiment.")
    parser.add_argument("--config", type=str, default="configs/default.json", help="Path to config JSON")
    args = parser.parse_args()

    config = ExperimentConfig.from_json(args.config)
    payload = run_experiment(config)
    output_file = save_experiment(payload, config.output_dir)

    print(json.dumps(payload, indent=2))
    print(f"\nSaved results to: {output_file}")


if __name__ == "__main__":
    main()
