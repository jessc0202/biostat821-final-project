"""Main processor for survey data pipeline."""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Union

from .aligner import align_waves
from .cleaner import handle_missing_values, remove_duplicates
from .loader import load_survey_files
from .mapper import map_columns, standardize_data_types
from .validator import check_missing_values, validate_required_columns


class SurveyProcessor:
    """Main class for processing survey data."""

    def __init__(
        self,
        default_mapping: Optional[Dict[str, List[str]]] = None,
        keep_all_columns: bool = True,
    ):
        self.combined_data: Optional[pd.DataFrame] = None
        self.default_mapping = default_mapping
        self.keep_all_columns = keep_all_columns

    def process_directory(
        self,
        directory: Union[str, Path],
        label: str,
        extensions: Optional[Sequence[str]] = None,
        file_patterns: Optional[Sequence[str]] = None,
    ) -> List[pd.DataFrame]:
        """Process a single directory of survey files.

        Args:
            directory: Directory with survey files.
            label: Label for the dataset group.
            extensions: Optional file extensions to load.
            file_patterns: Optional glob patterns to load.

        Returns:
            List of processed DataFrames.
        """
        raw_dfs = load_survey_files(
            directory,
            extensions=extensions,
            file_patterns=file_patterns,
        )

        processed_dfs: List[pd.DataFrame] = []
        for df in raw_dfs:
            df = map_columns(
                df,
                mapping=self.default_mapping,
                keep_all_columns=self.keep_all_columns,
            )
            df = standardize_data_types(df)
            df = remove_duplicates(
                df,
                subset=["response_id"] if "response_id" in df.columns else None,
            )
            df = handle_missing_values(
                df,
                strategy="drop",
                columns=["response_id"] if "response_id" in df.columns else None,
            )
            processed_dfs.append(df)

        return processed_dfs

    def process_data_groups(
        self,
        data_dirs: Dict[str, Union[str, Path]],
        extensions: Optional[Sequence[str]] = None,
        file_patterns: Optional[Sequence[str]] = None,
    ) -> pd.DataFrame:
        """Process and combine multiple labeled survey directories.

        Args:
            data_dirs: Mapping from label to directory path.
            extensions: Optional file extensions to load.
            file_patterns: Optional glob patterns to load.

        Returns:
            Combined DataFrame.
        """
        grouped_dfs: Dict[str, List[pd.DataFrame]] = {}
        for label, directory in data_dirs.items():
            grouped_dfs[label] = self.process_directory(
                directory,
                label,
                extensions=extensions,
                file_patterns=file_patterns,
            )

        self.combined_data = align_waves(grouped_dfs)
        return self.combined_data

    def process_all_data(
        self,
        usa_dir: Union[str, Path],
        argentina_dir: Union[str, Path],
        extensions: Optional[Sequence[str]] = None,
        file_patterns: Optional[Sequence[str]] = None,
    ) -> pd.DataFrame:
        """Process and combine USA and Argentina survey data.

        Args:
            usa_dir: Directory with USA survey files.
            argentina_dir: Directory with Argentina survey files.
            extensions: Optional file extensions to load.
            file_patterns: Optional glob patterns to load.

        Returns:
            Combined DataFrame.
        """
        return self.process_data_groups(
            {"USA": usa_dir, "Argentina": argentina_dir},
            extensions=extensions,
            file_patterns=file_patterns,
        )

    def validate_data(self, required_columns: Optional[List[str]] = None) -> Dict:
        """Validate the combined data.

        Args:
            required_columns: List of required columns.

        Returns:
            Validation results.
        """
        if self.combined_data is None:
            raise ValueError("No data to validate. Run process_data_groups first.")

        if required_columns is None:
            required_columns = ["group", "wave"]

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
            raise ValueError("No data to summarize. Run process_data_groups first.")

        summary = {
            "total_rows": len(self.combined_data),
            "total_columns": len(self.combined_data.columns),
            "waves": (
                sorted(self.combined_data["wave"].unique())
                if "wave" in self.combined_data.columns
                else []
            ),
            "groups": (
                self.combined_data["group"].unique().tolist()
                if "group" in self.combined_data.columns
                else []
            ),
            "columns": self.combined_data.columns.tolist(),
        }

        return summary
