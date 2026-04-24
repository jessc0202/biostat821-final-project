from __future__ import annotations

import tempfile
from pathlib import Path
from typing import ClassVar

import pandas as pd
import pytest

from dream_survey_processor.processor import SurveyProcessor


class TestSurveyProcessor:
    # Constants used for assertions across tests
    NUM_FILES: ClassVar[int] = 2
    ROWS_PER_FILE: ClassVar[int] = 2
    EXPECTED_ROWS: ClassVar[int] = 4
    EXPECTED_COLUMNS: ClassVar[int] = 5
    EXPECTED_WAVES: ClassVar[list[int]] = [1, 2]
    EXPECTED_GROUPS: ClassVar[set[str]] = {"USA", "Argentina"}

    def test_process_directory(self):
        """Test processing a single labeled directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            for i in range(self.NUM_FILES):
                data = {
                    "ResponseId": [f"id_{j}" for j in range(self.ROWS_PER_FILE)],
                    "Demo_Age": [25 + j for j in range(self.ROWS_PER_FILE)],
                    "StartDate": ["2024-01-01", "2024-01-02"],
                }
                df = pd.DataFrame(data)
                csv_path = Path(temp_dir) / f"wave_{i + 1}.csv"
                df.to_csv(csv_path, index=False)

            processor = SurveyProcessor()
            processed_dfs = processor.process_directory(temp_dir, "group")

            assert len(processed_dfs) == self.NUM_FILES
            for df in processed_dfs:
                assert "response_id" in df.columns
                assert "age" in df.columns
                assert "start_date" in df.columns
                assert len(df) == self.ROWS_PER_FILE

    def test_process_data_groups(self):
        """Test processing and combining multiple labeled directories."""
        with tempfile.TemporaryDirectory() as usa_dir, tempfile.TemporaryDirectory() as arg_dir:  # noqa: E501
            for i in range(2):
                data = {
                    "ResponseId": [f"usa_{j}" for j in range(2)],
                    "Demo_Age": [25 + j for j in range(2)],
                    "Demo_Gender": ["M", "F"],
                    "Dream_Text": ["Dream 1", "Dream 2"],
                }
                df = pd.DataFrame(data)

                df.to_csv(Path(usa_dir) / f"file_{i}.csv", index=False)
                df.to_csv(Path(arg_dir) / f"file_{i}.csv", index=False)

            processor = SurveyProcessor()
            data_dirs = {"USA": usa_dir, "Argentina": arg_dir}
            combined_df = processor.process_data_groups(data_dirs)

            expected_total_rows = 8
            assert len(combined_df) == expected_total_rows
            assert "group" in combined_df.columns
            assert "wave" in combined_df.columns
            assert set(combined_df["group"].unique()) == {"USA", "Argentina"}
            assert set(combined_df["wave"].unique()) == set(self.EXPECTED_WAVES)
            assert "response_id" in combined_df.columns

    def test_validate_data(self):
        """Test data validation."""
        processor = SurveyProcessor()
        data = {
            "response_id": [1, 2, 3],
            "wave": [1, 1, 2],
            "group": ["USA", "USA", "Argentina"],
            "age": [25, 30, 35],
        }
        processor.combined_data = pd.DataFrame(data)

        validation_results = processor.validate_data()

        assert "required_columns" in validation_results
        assert "missing_values" in validation_results
        assert all(validation_results["required_columns"].values())

    def test_validate_data_no_data(self):
        """Test validation when no data is processed."""
        processor = SurveyProcessor()

        with pytest.raises(ValueError, match="No data to validate"):
            processor.validate_data()

    def test_get_summary(self):
        """Test getting data summary."""
        processor = SurveyProcessor()
        data = {
            "response_id": [1, 2, 3, 4],
            "wave": [1, 1, 2, 2],
            "group": ["USA", "USA", "Argentina", "Argentina"],
            "age": [25, 30, 35, 40],
            "gender": ["M", "F", "M", "F"],
        }
        processor.combined_data = pd.DataFrame(data)

        summary = processor.get_summary()

        assert summary["total_rows"] == self.EXPECTED_ROWS
        assert summary["total_columns"] == self.EXPECTED_COLUMNS
        assert summary["waves"] == self.EXPECTED_WAVES
        assert set(summary["groups"]) == self.EXPECTED_GROUPS
        assert "response_id" in summary["columns"]

    def test_get_summary_no_data(self):
        """Test summary when no data is processed."""
        processor = SurveyProcessor()

        with pytest.raises(ValueError, match="No data to summarize"):
            processor.get_summary()
