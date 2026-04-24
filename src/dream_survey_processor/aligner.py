"""Module for aligning survey waves across datasets."""

from typing import Dict, List

import pandas as pd


def add_wave_column(
    dataframes: List[pd.DataFrame], wave_name: str = "wave"
) -> List[pd.DataFrame]:
    """Add a wave column to each DataFrame.

    Args:
        dataframes: List of DataFrames for each wave.
        wave_name: Name of the wave column.

    Returns:
        List of DataFrames with wave column added.
    """
    aligned_dfs = []
    for i, df in enumerate(dataframes):
        df_copy = df.copy()
        df_copy[wave_name] = i + 1  # Waves start from 1
        aligned_dfs.append(df_copy)
    return aligned_dfs


def align_waves(
    grouped_dataframes: Dict[str, List[pd.DataFrame]],
    group_name: str = "group",
    wave_name: str = "wave",
) -> pd.DataFrame:
    """Align waves from multiple labeled datasets.

    Args:
        grouped_dataframes: Mapping from group label to list of DataFrames.
        group_name: Name of the group label column.
        wave_name: Name of the wave column.

    Returns:
        Combined DataFrame with aligned waves and group labels.
    """
    aligned_dfs: List[pd.DataFrame] = []

    for label, dataframes in grouped_dataframes.items():
        group_dfs = add_wave_column(dataframes, wave_name=wave_name)
        for df in group_dfs:
            df[group_name] = label
        aligned_dfs.extend(group_dfs)

    if not aligned_dfs:
        return pd.DataFrame()

    combined_df = pd.concat(aligned_dfs, ignore_index=True, sort=False)
    return combined_df
