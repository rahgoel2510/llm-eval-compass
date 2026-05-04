#!/usr/bin/env python3
import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=0.05)
    parser.add_argument("--baseline-file", default="results/baseline.json")
    parser.add_argument("--current-file", default="results/current.json")
    args = parser.parse_args()

    with open(args.baseline_file) as f:
        baseline = json.load(f)
    with open(args.current_file) as f:
        current = json.load(f)

    failed = False
    for metric, base_val in baseline.items():
        cur_val = current.get(metric, 0)
        if base_val > 0 and (base_val - cur_val) / base_val > args.threshold:
            print(f"FAIL: {metric} dropped {base_val} -> {cur_val}")
            failed = True

    if failed:
        sys.exit(1)
    print("All metrics within threshold.")


if __name__ == "__main__":
    main()
