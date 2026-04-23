"""Module for mapping different survey schemas to a unified format."""

import pandas as pd
from typing import Dict, Any


# Define unified column names
UNIFIED_COLUMNS = {
    "response_id": ["ResponseId", "Response ID", "response_id"],
    "start_date": ["StartDate", "Start Date", "start_date"],
    "end_date": ["EndDate", "End Date", "end_date"],
    "progress": ["Progress", "progress"],
    "finished": ["Finished", "finished"],
    "duration": ["Duration (in seconds)", "duration"],
    "prolific_id": ["ProlificID", "PROLIFIC_PID", "prolific_id"],
    "age": ["Demo_Age", "age"],
    "gender": ["Demo_Gender", "gender"],
    "education": ["Demo_Education", "education"],
    # Add more mappings as needed
    "gad_bothered_1": ["GAD_Bothered_1", "gad_bothered_1"],
    "phq_bothered_1": ["PHQ_Bothered_1", "phq_bothered_1"],
    "sleep_quality": ["Sleep_Quality", "sleep_quality"],
    "dream_frequency": ["DreamQ_Frequency", "dream_frequency"],
    # Continue for all relevant columns
}


def map_columns(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """Map DataFrame columns to unified format.

    Args:
        df: Input DataFrame.
        country: Country name for specific mappings.

    Returns:
        DataFrame with unified column names.
    """
    column_mapping = {}

    for unified_name, possible_names in UNIFIED_COLUMNS.items():
        for possible_name in possible_names:
            if possible_name in df.columns:
                column_mapping[possible_name] = unified_name
                break

    # Rename columns
    df_renamed = df.rename(columns=column_mapping)

    # Keep only unified columns that exist
    existing_unified = [
        col for col in UNIFIED_COLUMNS.keys() if col in df_renamed.columns
    ]
    df_unified = df_renamed[existing_unified]

    return df_unified


def standardize_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize data types in the DataFrame.

    Args:
        df: Input DataFrame.

    Returns:
        DataFrame with standardized data types.
    """
    # Example standardizations
    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce")
    if "duration" in df.columns:
        df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
    if "start_date" in df.columns:
        df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    if "end_date" in df.columns:
        df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")

    return df
