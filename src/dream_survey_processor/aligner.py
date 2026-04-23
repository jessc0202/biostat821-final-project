"""Module for aligning survey waves across datasets."""

import pandas as pd
from typing import List


def add_wave_column(dataframes: List[pd.DataFrame], country: str) -> List[pd.DataFrame]:
    """Add a wave column to each DataFrame.

    Args:
        dataframes: List of DataFrames for each wave.
        country: Country name.

    Returns:
        List of DataFrames with wave column added.
    """
    aligned_dfs = []
    for i, df in enumerate(dataframes):
        df_copy = df.copy()
        df_copy["wave"] = i + 1  # Waves start from 1
        aligned_dfs.append(df_copy)
    return aligned_dfs


def align_waves(
    usa_dfs: List[pd.DataFrame], argentina_dfs: List[pd.DataFrame]
) -> pd.DataFrame:
    """Align waves from USA and Argentina datasets.

    Args:
        usa_dfs: List of USA DataFrames.
        argentina_dfs: List of Argentina DataFrames.

    Returns:
        Combined DataFrame with aligned waves.
    """
    # Add wave and country columns
    usa_aligned = add_wave_column(usa_dfs, "USA")
    argentina_aligned = add_wave_column(argentina_dfs, "Argentina")

    # Add country column
    for df in usa_aligned:
        df["country"] = "USA"
    for df in argentina_aligned:
        df["country"] = "Argentina"

    # Combine all DataFrames
    all_dfs = usa_aligned + argentina_aligned
    combined_df = pd.concat(all_dfs, ignore_index=True, sort=False)

    return combined_df
