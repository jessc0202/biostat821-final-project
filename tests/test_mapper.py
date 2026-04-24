"""Tests for the mapper module."""

import pandas as pd

from dream_survey_processor.mapper import map_columns, standardize_data_types


class TestMapper:
    """Test cases for data mapping functions."""

    def test_map_columns(self):
        """Test column mapping to unified format."""
        data = {
            "ResponseId": [1, 2, 3],
            "StartDate": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "Demo_Age": [25, 30, 35],
            "GAD_Bothered_1": [1, 2, 3],
            "extra_col": ["a", "b", "c"],
        }
        df = pd.DataFrame(data)

        mapped_df = map_columns(df, keep_all_columns=False)

        expected_columns = ["response_id", "start_date", "age", "gad_bothered_1"]
        for col in expected_columns:
            assert col in mapped_df.columns

        assert "extra_col" not in mapped_df.columns

    def test_map_columns_preserves_extra_columns(self):
        """Test that extra columns are preserved when requested."""
        data = {
            "ResponseId": [1, 2, 3],
            "StartDate": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "extra_col": ["a", "b", "c"],
        }
        df = pd.DataFrame(data)

        mapped_df = map_columns(df, keep_all_columns=True)

        assert "extra_col" in mapped_df.columns
        assert "response_id" in mapped_df.columns

    def test_standardize_data_types(self):
        """Test data type standardization."""
        data = {
            "age": ["25", "30", "35"],
            "duration": ["100", "200", "300"],
            "start_date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "text_col": ["a", "b", "c"],
        }
        df = pd.DataFrame(data)

        standardized_df = standardize_data_types(df)

        assert pd.api.types.is_numeric_dtype(standardized_df["age"])
        assert pd.api.types.is_numeric_dtype(standardized_df["duration"])
        assert pd.api.types.is_datetime64_any_dtype(standardized_df["start_date"])
        assert standardized_df["text_col"].dtype == object
