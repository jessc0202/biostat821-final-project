"""Module for cleaning survey data."""

from typing import List

import pandas as pd


def remove_duplicates(df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
    """Remove duplicate rows.

    Args:
        df: DataFrame to clean.
        subset: Columns to consider for duplicates.

    Returns:
        DataFrame with duplicates removed.
    """
    return df.drop_duplicates(subset=subset)


def handle_missing_values(
    df: pd.DataFrame, strategy: str = "drop", columns: List[str] = None
) -> pd.DataFrame:
    """Handle missing values.

    Args:
        df: DataFrame to clean.
        strategy: Strategy ('drop', 'fill_mean', 'fill_median', 'fill_mode').
        columns: Columns to apply strategy to.

    Returns:
        DataFrame with missing values handled.
    """
    if columns is None:
        columns = df.columns

    if strategy == "drop":
        return df.dropna(subset=columns)
    if strategy == "fill_mean":
        for col in columns:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
    elif strategy == "fill_median":
        for col in columns:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
    elif strategy == "fill_mode":
        for col in columns:
            if col in df.columns:
                df[col] = df[col].fillna(
                    df[col].mode().iloc[0] if not df[col].mode().empty else df[col]
                )

    return df


def normalize_text(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Normalize text columns (strip, lowercase).

    Args:
        df: DataFrame to clean.
        columns: Text columns to normalize.

    Returns:
        DataFrame with normalized text.
    """
    for col in columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
    return df
