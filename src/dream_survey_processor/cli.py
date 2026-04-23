"""Command-line interface for the survey processor."""

import argparse
import sys
from pathlib import Path

from .processor import SurveyProcessor


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Process multi-wave survey data.")
    parser.add_argument(
        "--usa-dir", required=True, help="Directory with USA survey files"
    )
    parser.add_argument(
        "--argentina-dir", required=True, help="Directory with Argentina survey files"
    )
    parser.add_argument(
        "--output", "-o", help="Output file path for processed data (CSV)"
    )
    parser.add_argument(
        "--validate", action="store_true", help="Run validation on processed data"
    )

    args = parser.parse_args()

    # Check directories exist
    usa_path = Path(args.usa_dir)
    arg_path = Path(args.argentina_dir)

    if not usa_path.exists():
        print(f"Error: USA directory {usa_path} does not exist")
        sys.exit(1)
    if not arg_path.exists():
        print(f"Error: Argentina directory {arg_path} does not exist")
        sys.exit(1)

    # Process data
    processor = SurveyProcessor()
    try:
        combined_data = processor.process_all_data(usa_path, arg_path)
        print(f"Successfully processed {len(combined_data)} rows of data")

        # Validation
        if args.validate:
            validation_results = processor.validate_data()
            print("Validation results:")
            print(
                f"Required columns present: {all(validation_results['required_columns'].values())}"
            )
            if validation_results["missing_values"]:
                print(
                    f"Columns with high missing values: {validation_results['missing_values']}"
                )

        # Output
        if args.output:
            output_path = Path(args.output)
            combined_data.to_csv(output_path, index=False)
            print(f"Data saved to {output_path}")
        else:
            # Print summary
            summary = processor.get_summary()
            print("Data summary:")
            for key, value in summary.items():
                print(f"  {key}: {value}")

    except Exception as e:
        print(f"Error processing data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
