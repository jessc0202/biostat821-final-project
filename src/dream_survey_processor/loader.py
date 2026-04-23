"""Module for loading survey data from CSV and Excel files."""

import pandas as pd
from pathlib import Path
from typing import Union, List


def load_csv(file_path: Union[str, Path]) -> pd.DataFrame:
    """Load data from a CSV file.

    Args:
        file_path: Path to the CSV file.

    Returns:
        DataFrame containing the loaded data.
    """
    return pd.read_csv(file_path)


def load_excel(file_path: Union[str, Path], sheet_name: str = 0) -> pd.DataFrame:
    """Load data from an Excel file.

    Args:
        file_path: Path to the Excel file.
        sheet_name: Name or index of the sheet to load.

    Returns:
        DataFrame containing the loaded data.
    """
    return pd.read_excel(file_path, sheet_name=sheet_name)


def load_survey_files(directory: Union[str, Path], country: str) -> List[pd.DataFrame]:
    """Load all survey files for a given country.

    Args:
        directory: Directory containing the survey files.
        country: Country name ('USA' or 'Argentina').

    Returns:
        List of DataFrames, one for each wave.
    """
    dir_path = Path(directory)
    dataframes = []

    if country == "USA":
        # USA has CSV files
        csv_files = sorted(dir_path.glob("*.csv"))
        for csv_file in csv_files:
            df = load_csv(csv_file)
            dataframes.append(df)
    elif country == "Argentina":
        # Argentina has Excel files
        excel_files = sorted(dir_path.glob("*.xlsx"))
        for excel_file in excel_files:
            df = load_excel(excel_file)
            dataframes.append(df)
    else:
        raise ValueError(f"Unsupported country: {country}")

    return dataframes
