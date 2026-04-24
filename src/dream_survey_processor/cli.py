"""Command-line interface for the survey processor."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .processor import SurveyProcessor


def parse_input_dirs(values: list[str]) -> dict[str, Path]:
    """Parse input directories in label=path format."""
    parsed: dict[str, Path] = {}
    msg = "Each --input-dir entry must be in the form label=path"
    for item in values:
        if "=" not in item:
            raise ValueError(msg)
        label, path = item.split("=", 1)
        if not label or not path:
            raise ValueError(msg)
        parsed[label] = Path(path)
    return parsed


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Process multi-wave survey data.")
    parser.add_argument(
        "--input-dir",
        action="append",
        required=True,
        help="Input directory in the form label=path. Repeat for multiple datasets.",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path for processed data (CSV)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run validation on processed data",
    )

    args = parser.parse_args()

    try:
        data_dirs = parse_input_dirs(args.input_dir)
    except ValueError as exc:
        err_msg = f"Error: {exc}"
        print(err_msg, file=sys.stderr)  # noqa: T201
        sys.exit(1)

    missing_dirs = [label for label, path in data_dirs.items() if not path.exists()]
    if missing_dirs:
        err_msg = f"Error: Missing directories: {', '.join(missing_dirs)}"
        print(err_msg, file=sys.stderr)  # noqa: T201
        sys.exit(1)

    processor = SurveyProcessor()
    try:
        combined_data = processor.process_data_groups(data_dirs)
        print(f"Successfully processed {len(combined_data)} rows of data")  # noqa: T201

        if args.validate:
            validation_results = processor.validate_data()
            print("Validation results:")  # noqa: T201
            has_all_cols = all(validation_results["required_columns"].values())
            print(f"  required columns present: {has_all_cols}")  # noqa: T201
            if validation_results["missing_values"]:
                msg = (
                    f"  columns with high missing values: "
                    f"{validation_results['missing_values']}"
                )
                print(msg)  # noqa: T201

        if args.output:
            output_path = Path(args.output)
            combined_data.to_csv(output_path, index=False)
            print(f"Data saved to {output_path}")  # noqa: T201
        else:
            summary = processor.get_summary()
            print("Data summary:")  # noqa: T201
            for key, value in summary.items():
                print(f"  {key}: {value}")  # noqa: T201

    except ValueError as exc:
        err_msg = f"Error processing data: {exc}"
        print(err_msg, file=sys.stderr)  # noqa: T201
        sys.exit(1)


if __name__ == "__main__":
    main()
