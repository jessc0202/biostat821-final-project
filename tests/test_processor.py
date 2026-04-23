"""Tests for the processor module."""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os

from dream_survey_processor.processor import SurveyProcessor


class TestSurveyProcessor:
    """Test cases for the SurveyProcessor class."""

    def test_process_country_data(self):
        """Test processing data for a single country."""
        # Create temporary directory with CSV files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create sample CSV files
            for i in range(2):
                data = {
                    "ResponseId": [f"id_{j}" for j in range(2)],
                    "Demo_Age": [25 + j for j in range(2)],
                    "StartDate": ["2024-01-01", "2024-01-02"],
                }
                df = pd.DataFrame(data)
                csv_path = Path(temp_dir) / f"wave_{i+1}.csv"
                df.to_csv(csv_path, index=False)

            processor = SurveyProcessor()
            processed_dfs = processor.process_country_data(temp_dir, "USA")

            assert len(processed_dfs) == 2
            for df in processed_dfs:
                assert "response_id" in df.columns
                assert "age" in df.columns
                assert "start_date" in df.columns
                assert len(df) == 2

    def test_process_all_data(self):
        """Test processing and combining data from both countries."""
        # Create temporary directories
        with tempfile.TemporaryDirectory() as usa_dir, tempfile.TemporaryDirectory() as arg_dir:
            # Create USA CSV files
            for i in range(2):
                data = {
                    "ResponseId": [f"usa_{j}" for j in range(2)],
                    "Demo_Age": [25 + j for j in range(2)],
                }
                df = pd.DataFrame(data)
                csv_path = Path(usa_dir) / f"usa_wave_{i+1}.csv"
                df.to_csv(csv_path, index=False)

            # Create Argentina Excel files
            for i in range(2):
                data = {
                    "ResponseId": [f"arg_{j}" for j in range(2)],
                    "Demo_Age": [35 + j for j in range(2)],
                }
                df = pd.DataFrame(data)
                excel_path = Path(arg_dir) / f"arg_form_{i+1}.xlsx"
                df.to_excel(excel_path, index=False)

            processor = SurveyProcessor()
            combined_df = processor.process_all_data(usa_dir, arg_dir)

            # Check combined data
            assert len(combined_df) == 8  # 2 countries * 2 waves * 2 rows
            assert "wave" in combined_df.columns
            assert "country" in combined_df.columns
            assert set(combined_df["country"].unique()) == {"USA", "Argentina"}
            assert set(combined_df["wave"].unique()) == {1, 2}

    def test_validate_data(self):
        """Test data validation."""
        processor = SurveyProcessor()
        # Create mock combined data
        data = {
            "response_id": [1, 2, 3],
            "wave": [1, 1, 2],
            "country": ["USA", "USA", "Argentina"],
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
        # Create mock combined data
        data = {
            "response_id": [1, 2, 3, 4],
            "wave": [1, 1, 2, 2],
            "country": ["USA", "USA", "Argentina", "Argentina"],
            "age": [25, 30, 35, 40],
            "gender": ["M", "F", "M", "F"],
        }
        processor.combined_data = pd.DataFrame(data)

        summary = processor.get_summary()

        assert summary["total_rows"] == 4
        assert summary["total_columns"] == 5
        assert summary["waves"] == [1, 2]
        assert set(summary["countries"]) == {"USA", "Argentina"}
        assert "response_id" in summary["columns"]

    def test_get_summary_no_data(self):
        """Test summary when no data is processed."""
        processor = SurveyProcessor()

        with pytest.raises(ValueError, match="No data to summarize"):
            processor.get_summary()
