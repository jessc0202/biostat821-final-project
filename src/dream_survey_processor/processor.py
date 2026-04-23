"""Main processor for survey data pipeline."""

import pandas as pd
from pathlib import Path
from typing import Union, List

from .loader import load_survey_files
from .mapper import map_columns, standardize_data_types
from .aligner import align_waves
from .validator import validate_required_columns, check_missing_values
from .cleaner import remove_duplicates, handle_missing_values


class SurveyProcessor:
    """Main class for processing survey data."""

    def __init__(self):
        self.combined_data = None

    def process_country_data(
        self, directory: Union[str, Path], country: str
    ) -> List[pd.DataFrame]:
        """Process data for a single country.

        Args:
            directory: Directory with survey files.
            country: Country name.

        Returns:
            List of processed DataFrames.
        """
        # Load data
        raw_dfs = load_survey_files(directory, country)

        # Process each wave
        processed_dfs = []
        for df in raw_dfs:
            # Map columns
            df = map_columns(df, country)
            # Standardize types
            df = standardize_data_types(df)
            # Basic cleaning
            df = remove_duplicates(
                df, subset=["response_id"] if "response_id" in df.columns else None
            )
            df = handle_missing_values(df, strategy="drop", columns=["response_id"])
            processed_dfs.append(df)

        return processed_dfs

    def process_all_data(
        self, usa_dir: Union[str, Path], argentina_dir: Union[str, Path]
    ) -> pd.DataFrame:
        """Process and combine data from both countries.

        Args:
            usa_dir: Directory with USA survey files.
            argentina_dir: Directory with Argentina survey files.

        Returns:
            Combined DataFrame.
        """
        # Process each country
        usa_dfs = self.process_country_data(usa_dir, "USA")
        argentina_dfs = self.process_country_data(argentina_dir, "Argentina")

        # Align and combine
        self.combined_data = align_waves(usa_dfs, argentina_dfs)

        return self.combined_data

    def validate_data(self, required_columns: List[str] = None) -> Dict:
        """Validate the combined data.

        Args:
            required_columns: List of required columns.

        Returns:
            Validation results.
        """
        if self.combined_data is None:
            raise ValueError("No data to validate. Run process_all_data first.")

        if required_columns is None:
            required_columns = ["response_id", "wave", "country"]

        results = {
            "required_columns": validate_required_columns(
                self.combined_data, required_columns
            ),
            "missing_values": check_missing_values(self.combined_data),
        }

        return results

    def get_summary(self) -> Dict:
        """Get summary statistics of the data.

        Returns:
            Dictionary with summary info.
        """
        if self.combined_data is None:
            raise ValueError("No data to summarize. Run process_all_data first.")

        summary = {
            "total_rows": len(self.combined_data),
            "total_columns": len(self.combined_data.columns),
            "waves": sorted(self.combined_data["wave"].unique()),
            "countries": self.combined_data["country"].unique().tolist(),
            "columns": self.combined_data.columns.tolist(),
        }

        return summary
