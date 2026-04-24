"""Tests for the loader module."""

import os
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from dream_survey_processor.loader import load_csv, load_excel, load_survey_files


class TestLoader:
    """Test cases for data loading functions."""

    # Constants for test assertions
    NUM_FILES = 2
    ROWS_PER_FILE = 3

    def test_load_csv(self):
        """Test loading a CSV file."""
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
        data = {"col1": [1, 2, 3], "col2": ["a", "b", "c"]}
        df = pd.DataFrame(data)

        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            df.to_excel(f, index=False)
            excel_path = f.name

        try:
            loaded_df = load_excel(excel_path)
            assert list(loaded_df.columns) == list(df.columns)
            assert len(loaded_df) == len(df)
        finally:
            os.unlink(excel_path)

    def test_load_survey_files_csv(self):
        """Test loading survey CSV files from a directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            for i in range(2):
                data = {
                    "ResponseId": [f"id_{j}" for j in range(3)],
                    "value": [i * 3 + j for j in range(3)],
                }
                df = pd.DataFrame(data)
                csv_path = Path(temp_dir) / f"file_{i}.csv"
                df.to_csv(csv_path, index=False)

            loaded_dfs = load_survey_files(temp_dir, extensions=[".csv"])
            assert len(loaded_dfs) == self.NUM_FILES
            for df in loaded_dfs:
                assert "ResponseId" in df.columns
                assert len(df) == self.ROWS_PER_FILE

    def test_load_survey_files_excel(self):
        """Test loading survey Excel files from a directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            for i in range(2):
                data = {
                    "ResponseId": [f"id_{j}" for j in range(3)],
                    "value": [i * 3 + j for j in range(3)],
                }
                df = pd.DataFrame(data)
                excel_path = Path(temp_dir) / f"file_{i}.xlsx"
                df.to_excel(excel_path, index=False)

            loaded_dfs = load_survey_files(temp_dir, extensions=[".xlsx"])
            assert len(loaded_dfs) == self.NUM_FILES
            for df in loaded_dfs:
                assert "ResponseId" in df.columns
                assert len(df) == self.ROWS_PER_FILE

    def test_load_survey_files_invalid_directory(self):
        """Test loading files from a missing directory."""
        with pytest.raises(ValueError, match="Directory does not exist"):
            load_survey_files("/path/does/not/exist")
