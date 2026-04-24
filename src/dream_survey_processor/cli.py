"""Command-line interface for the survey processor."""

import argparse
import sys
from pathlib import Path
from typing import Dict

from .processor import SurveyProcessor


def parse_input_dirs(values: list[str]) -> Dict[str, Path]:
    parsed: Dict[str, Path] = {}
    for item in values:
        if "=" not in item:
            raise ValueError("Each --input-dir entry must be in the form label=path")
        label, path = item.split("=", 1)
        if not label or not path:
            raise ValueError("Each --input-dir entry must be in the form label=path")
        parsed[label] = Path(path)
    return parsed


def main():
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
        print(f"Error: {exc}")
        sys.exit(1)

    missing_dirs = [label for label, path in data_dirs.items() if not path.exists()]
    if missing_dirs:
        print(f"Error: Missing directories: {', '.join(missing_dirs)}")
        sys.exit(1)

    processor = SurveyProcessor()
    try:
        combined_data = processor.process_data_groups(data_dirs)
        print(f"Successfully processed {len(combined_data)} rows of data")

        if args.validate:
            validation_results = processor.validate_data()
            print("Validation results:")
            print(
                f"  required columns present: {all(validation_results['required_columns'].values())}"
            )
            if validation_results["missing_values"]:
                print(
                    f"  columns with high missing values: {validation_results['missing_values']}"
                )

        if args.output:
            output_path = Path(args.output)
            combined_data.to_csv(output_path, index=False)
            print(f"Data saved to {output_path}")
        else:
            summary = processor.get_summary()
            print("Data summary:")
            for key, value in summary.items():
                print(f"  {key}: {value}")

    except Exception as e:
        print(f"Error processing data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
