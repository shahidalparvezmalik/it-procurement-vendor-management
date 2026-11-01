"""Command line for the synthetic procurement management demo."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Sequence

from .io import load_contracts, write_reports


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create review-only scorecards from synthetic contract data.")
    parser.add_argument("--input", default="data/contracts.csv", help="Input contracts CSV")
    parser.add_argument("--output-dir", default="reports", help="Output directory")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Assessment date YYYY-MM-DD")
    args = parser.parse_args(argv)
    try:
        as_of = date.fromisoformat(args.as_of)
        records = load_contracts(args.input, as_of)
        outputs = write_reports(records, args.output_dir, as_of)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(f"Contracts assessed: {len(records)}")
    print("Assessment method: transparent rules baseline (not an AI model)")
    print("Human review required: yes; no procurement actions are executed")
    for label, path in outputs.items():
        print(f"{label}: {Path(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
