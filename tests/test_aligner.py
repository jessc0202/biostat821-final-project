"""Tests for the aligner module."""

import pytest
import pandas as pd

from dream_survey_processor.aligner import add_wave_column, align_waves


class TestAligner:
    """Test cases for data alignment functions."""

    def test_add_wave_column(self):
        """Test adding wave column to DataFrames."""
        dfs = [
            pd.DataFrame({"id": [1, 2], "value": [10, 20]}),
            pd.DataFrame({"id": [3, 4], "value": [30, 40]}),
            pd.DataFrame({"id": [5, 6], "value": [50, 60]}),
        ]

        aligned_dfs = add_wave_column(dfs, "USA")

        assert len(aligned_dfs) == 3
        for i, df in enumerate(aligned_dfs):
            assert "wave" in df.columns
            assert all(df["wave"] == i + 1)
            assert "id" in df.columns
            assert "value" in df.columns

    def test_align_waves(self):
        """Test aligning waves from different countries."""
        usa_dfs = [
            pd.DataFrame({"response_id": [1, 2], "age": [25, 30]}),
            pd.DataFrame({"response_id": [1, 2], "age": [26, 31]}),
        ]
        argentina_dfs = [
            pd.DataFrame({"response_id": [3, 4], "age": [35, 40]}),
            pd.DataFrame({"response_id": [3, 4], "age": [36, 41]}),
        ]

        combined_df = align_waves(usa_dfs, argentina_dfs)

        # Check total rows
        assert len(combined_df) == 8  # 2 waves * 2 countries * 2 rows each

        # Check columns
        assert "wave" in combined_df.columns
        assert "country" in combined_df.columns
        assert "response_id" in combined_df.columns
        assert "age" in combined_df.columns

        # Check wave values
        assert set(combined_df["wave"].unique()) == {1, 2}

        # Check country values
        assert set(combined_df["country"].unique()) == {"USA", "Argentina"}
