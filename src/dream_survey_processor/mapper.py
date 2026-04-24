"""Module for mapping different survey schemas to a unified format."""

import pandas as pd
from typing import Dict, List, Optional


DEFAULT_COLUMN_MAPPING: Dict[str, List[str]] = {
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
}


def _build_column_map(mapping: Dict[str, List[str]]) -> Dict[str, str]:
    """Build a source-to-target column map from mapping values."""
    column_map: Dict[str, str] = {}
    for target_name, source_names in mapping.items():
        for source_name in source_names:
            column_map[source_name] = target_name
    return column_map


def map_columns(
    df: pd.DataFrame,
    mapping: Optional[Dict[str, List[str]]] = None,
    keep_all_columns: bool = True,
) -> pd.DataFrame:
    """Map DataFrame columns to a unified format.

    Args:
        df: Input DataFrame.
        mapping: Optional mapping from target name to possible source names.
        keep_all_columns: If True, preserve columns that are not mapped.

    Returns:
        DataFrame with unified column names.
    """
    if mapping is None:
        mapping = DEFAULT_COLUMN_MAPPING

    source_to_target = _build_column_map(mapping)
    rename_map = {
        column_name: source_to_target[column_name]
        for column_name in df.columns
        if column_name in source_to_target
    }

    renamed_df = df.rename(columns=rename_map)

    if keep_all_columns:
        return renamed_df

    mapped_columns = [
        source_to_target[col] for col in df.columns if col in source_to_target
    ]
    return renamed_df[mapped_columns]


def standardize_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize data types in the DataFrame.

    Args:
        df: Input DataFrame.

    Returns:
        DataFrame with standardized data types.
    """
    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce")
    if "duration" in df.columns:
        df["duration"] = pd.to_numeric(df["duration"], errors="coerce")
    if "start_date" in df.columns:
        df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    if "end_date" in df.columns:
        df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")

    return df
