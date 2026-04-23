"""Tests for the loader module."""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os

from dream_survey_processor.loader import load_csv, load_excel, load_survey_files


class TestLoader:
    """Test cases for data loading functions."""

    def test_load_csv(self):
        """Test loading a CSV file."""
        # Create a temporary CSV file
        data = {"col1": [1, 2, 3], "col2": ["a", "b", "c"]}
        df = pd.DataFrame(data)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            df.to_csv(f, index=False)
            csv_path = f.name

        try:
            loaded_df = load_csv(csv_path)
            pd.testing.assert_frame_equal(loaded_df, df)
        finally:
            os.unlink(csv_path)

    def test_load_excel(self):
        """Test loading an Excel file."""
        # Create a temporary Excel file
        data = {"col1": [1, 2, 3], "col2": ["a", "b", "c"]}
        df = pd.DataFrame(data)

        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            df.to_excel(f, index=False)
            excel_path = f.name

        try:
            loaded_df = load_excel(excel_path)
            # Note: Excel loading might have slight differences, check columns
            assert list(loaded_df.columns) == list(df.columns)
            assert len(loaded_df) == len(df)
        finally:
            os.unlink(excel_path)

    def test_load_survey_files_usa(self):
        """Test loading USA survey files."""
        # Create temporary directory with CSV files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create sample CSV files
            for i in range(2):
                data = {
                    "ResponseId": [f"id_{j}" for j in range(3)],
                    "value": [i * 3 + j for j in range(3)],
                }
                df = pd.DataFrame(data)
                csv_path = Path(temp_dir) / f"file_{i}.csv"
                df.to_csv(csv_path, index=False)

            loaded_dfs = load_survey_files(temp_dir, "USA")
            assert len(loaded_dfs) == 2
            for df in loaded_dfs:
                assert "ResponseId" in df.columns
                assert len(df) == 3

    def test_load_survey_files_argentina(self):
        """Test loading Argentina survey files."""
        # Create temporary directory with Excel files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create sample Excel files
            for i in range(2):
                data = {
                    "ResponseId": [f"id_{j}" for j in range(3)],
                    "value": [i * 3 + j for j in range(3)],
                }
                df = pd.DataFrame(data)
                excel_path = Path(temp_dir) / f"file_{i}.xlsx"
                df.to_excel(excel_path, index=False)

            loaded_dfs = load_survey_files(temp_dir, "Argentina")
            assert len(loaded_dfs) == 2
            for df in loaded_dfs:
                assert "ResponseId" in df.columns
                assert len(df) == 3

    def test_load_survey_files_invalid_country(self):
        """Test loading with invalid country."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(ValueError, match="Unsupported country"):
                load_survey_files(temp_dir, "Invalid")
