"""Main processor for survey data pipeline."""

from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

from .aligner import align_waves
from .cleaner import handle_missing_values, remove_duplicates
from .loader import load_survey_files
from .mapper import map_columns, standardize_data_types
from .validator import check_missing_values, validate_required_columns

if TYPE_CHECKING:
    from pathlib import Path

    import pandas as pd


class SurveyProcessor:
    """Main class for processing survey data."""

    def __init__(
        self,
        default_mapping: dict[str, list[str]] | None = None,
        *,
        keep_all_columns: bool = True,
    ):
        self.combined_data: pd.DataFrame | None = None
        self.default_mapping = default_mapping
        self.keep_all_columns = keep_all_columns

    def process_directory(
        self,
        directory: str | Path,
        label: str,  # noqa: ARG002
        extensions: Sequence[str] | None = None,
        file_patterns: Sequence[str] | None = None,
    ) -> list[pd.DataFrame]:
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

        processed_dfs: list[pd.DataFrame] = []

        for raw_df in raw_dfs:
            # 1. Map columns using the provided schema
            mapped_df = map_columns(
                raw_df,
                mapping=self.default_mapping,
                keep_all_columns=self.keep_all_columns,
            )

            # 2. Standardize types (e.g., dates, numeric)
            standardized_df = standardize_data_types(mapped_df)

            # 3. Remove duplicates based on ID if it exists
            id_col = (
                ["response_id"] if "response_id" in standardized_df.columns else None
            )
            deduplicated_df = remove_duplicates(
                standardized_df,
                subset=id_col,
            )

            # 4. Clean missing values
            final_df = handle_missing_values(
                deduplicated_df,
                strategy="drop",
                columns=id_col,
            )

            processed_dfs.append(final_df)

        return processed_dfs

    def process_data_groups(
        self,
        data_dirs: dict[str, str | Path],
        extensions: Sequence[str] | None = None,
        file_patterns: Sequence[str] | None = None,
    ) -> pd.DataFrame:
        """Process and combine multiple labeled survey directories.

        Args:
            data_dirs: Mapping from label to directory path.
            extensions: Optional file extensions to load.
            file_patterns: Optional glob patterns to load.

        Returns:
            Combined DataFrame.
        """
        grouped_dfs: dict[str, list[pd.DataFrame]] = {}
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
        usa_dir: str | Path,
        argentina_dir: str | Path,
        extensions: Sequence[str] | None = None,
        file_patterns: Sequence[str] | None = None,
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

    def validate_data(self, required_columns: list[str] | None = None) -> dict:
        """Validate the combined data.

        Args:
            required_columns: List of required columns.

        Returns:
            Validation results.
        """
        if self.combined_data is None:
            msg = "No data to validate. Run process_data_groups first."
            raise ValueError(msg)

        if required_columns is None:
            required_columns = ["group", "wave"]

        return {
            "required_columns": validate_required_columns(
                self.combined_data, required_columns
            ),
            "missing_values": check_missing_values(self.combined_data),
        }

    def get_summary(self) -> dict:
        """Get summary statistics of the data.

        Returns:
            Dictionary with summary info.
        """
        if self.combined_data is None:
            msg = "No data to summarize. Run process_data_groups first."
            raise ValueError(msg)

        return {
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
