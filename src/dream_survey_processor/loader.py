"""Module for loading survey data from CSV and Excel files."""

import pandas as pd
from pathlib import Path
from typing import List, Optional, Sequence, Union

SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def load_csv(file_path: Union[str, Path]) -> pd.DataFrame:
    """Load data from a CSV file.

    Args:
        file_path: Path to the CSV file.

    Returns:
        DataFrame containing the loaded data.
    """
    return pd.read_csv(file_path)


def load_excel(
    file_path: Union[str, Path], sheet_name: Union[int, str] = 0
) -> pd.DataFrame:
    """Load data from an Excel file.

    Args:
        file_path: Path to the Excel file.
        sheet_name: Name or index of the sheet to load.

    Returns:
        DataFrame containing the loaded data.
    """
    return pd.read_excel(file_path, sheet_name=sheet_name)


def load_survey_files(
    directory: Union[str, Path],
    extensions: Optional[Sequence[str]] = None,
    file_patterns: Optional[Sequence[str]] = None,
    sheet_name: Union[int, str] = 0,
) -> List[pd.DataFrame]:
    """Load survey files from a directory.

    Args:
        directory: Directory containing survey files.
        extensions: Optional list of file extensions to load.
        file_patterns: Optional list of glob patterns to load.
        sheet_name: Sheet name or index for Excel files.

    Returns:
        List of DataFrames, one for each file.
    """
    dir_path = Path(directory)
    if not dir_path.exists() or not dir_path.is_dir():
        raise ValueError(f"Directory does not exist: {directory}")

    if file_patterns is None:
        if extensions is None:
            extensions = tuple(SUPPORTED_EXTENSIONS)
        file_patterns = [f"*{ext}" for ext in extensions]

    matched_files: List[Path] = []
    for pattern in file_patterns:
        matched_files.extend(sorted(dir_path.glob(pattern)))

    unique_files = list(dict.fromkeys(matched_files))
    dataframes: List[pd.DataFrame] = []

    for file_path in unique_files:
        suffix = file_path.suffix.lower()
        if suffix == ".csv":
            dataframes.append(load_csv(file_path))
        elif suffix in {".xlsx", ".xls"}:
            dataframes.append(load_excel(file_path, sheet_name=sheet_name))
        else:
            continue

    return dataframes
