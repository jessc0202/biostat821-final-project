"""Module for validating survey data."""

import pandas as pd
from typing import List, Dict


def validate_required_columns(
    df: pd.DataFrame, required_columns: List[str]
) -> Dict[str, bool]:
    """Check if required columns are present.

    Args:
        df: DataFrame to validate.
        required_columns: List of required column names.

    Returns:
        Dictionary with column presence status.
    """
    validation_results = {}
    for col in required_columns:
        validation_results[col] = col in df.columns
    return validation_results


def validate_data_types(
    df: pd.DataFrame, expected_types: Dict[str, str]
) -> Dict[str, bool]:
    """Check if columns have expected data types.

    Args:
        df: DataFrame to validate.
        expected_types: Dictionary of column to expected type.

    Returns:
        Dictionary with type validation status.
    """
    validation_results = {}
    for col, expected_type in expected_types.items():
        if col in df.columns:
            actual_type = str(df[col].dtype)
            validation_results[col] = actual_type == expected_type
        else:
            validation_results[col] = False
    return validation_results


def check_missing_values(df: pd.DataFrame, threshold: float = 0.5) -> Dict[str, float]:
    """Check for columns with high missing value rates.

    Args:
        df: DataFrame to check.
        threshold: Threshold for flagging high missing rates.

    Returns:
        Dictionary of columns with missing rates above threshold.
    """
    missing_rates = df.isnull().mean()
    high_missing = missing_rates[missing_rates > threshold]
    return high_missing.to_dict()
