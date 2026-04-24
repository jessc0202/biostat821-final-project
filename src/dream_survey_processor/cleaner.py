from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


def remove_duplicates(
    df: pd.DataFrame, subset: list[str] | None = None
) -> pd.DataFrame:
    """Remove duplicate rows.

    Args:
        df: DataFrame to clean.
        subset: Columns to consider for duplicates.

    Returns:
        DataFrame with duplicates removed.
    """
    return df.drop_duplicates(subset=subset)


def handle_missing_values(
    df: pd.DataFrame, strategy: str = "drop", columns: list[str] | None = None
) -> pd.DataFrame:
    """Handle missing values in the DataFrame."""
    if df is None or df.empty:
        return df

    if strategy == "drop":
        return df.dropna(subset=columns)

    if strategy == "fill":
        return df.fillna(0)

    return df


def normalize_text(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
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
