"""Tests for the aligner module."""

import pandas as pd

from dream_survey_processor.aligner import add_wave_column, align_waves


class TestAligner:
    """Test cases for data alignment functions."""

    # Constants for test assertions
    NUM_FILES = 3
    TOTAL_ROWS = 8
    EXPECTED_WAVES = {1, 2}
    EXPECTED_GROUPS = {"USA", "Argentina"}

    def test_add_wave_column(self):
        """Test adding wave column to DataFrames."""
        dfs = [
            pd.DataFrame({"id": [1, 2], "value": [10, 20]}),
            pd.DataFrame({"id": [3, 4], "value": [30, 40]}),
            pd.DataFrame({"id": [5, 6], "value": [50, 60]}),
        ]

        aligned_dfs = add_wave_column(dfs)

        assert len(aligned_dfs) == self.NUM_FILES
        for i, df in enumerate(aligned_dfs):
            assert "wave" in df.columns
            assert all(df["wave"] == i + 1)
            assert "id" in df.columns
            assert "value" in df.columns

    def test_align_waves(self):
        """Test aligning waves from different groups."""
        usa_dfs = [
            pd.DataFrame({"response_id": [1, 2], "age": [25, 30]}),
            pd.DataFrame({"response_id": [1, 2], "age": [26, 31]}),
        ]
        argentina_dfs = [
            pd.DataFrame({"response_id": [3, 4], "age": [35, 40]}),
            pd.DataFrame({"response_id": [3, 4], "age": [36, 41]}),
        ]

        combined_df = align_waves({"USA": usa_dfs, "Argentina": argentina_dfs})

        assert len(combined_df) == self.TOTAL_ROWS
        assert "wave" in combined_df.columns
        assert "group" in combined_df.columns
        assert "response_id" in combined_df.columns
        assert "age" in combined_df.columns
        assert set(combined_df["wave"].unique()) == self.EXPECTED_WAVES
        assert set(combined_df["group"].unique()) == self.EXPECTED_GROUPS
