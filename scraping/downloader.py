"""
data_downloader.py

This module defines a class for downloading structured JSON datasets
(match data, detailed match data, and player statistics) from a remote
data server. It supports organizing the data by competition and year.

Requires:
    - requests
    - ENVIRONMENT_VARIABLES.py containing `DATA_WEBSITE`
"""

import os
import sys
import requests
import json
from typing import List, Callable

# Add parent directory to path to import environment variables
sys.path.append('..')
import ENVIRONMENT_VARIABLES as EV

# Configurable constants
SELECTION_TYPE: List[str] = ['HOSTPLUS']
YEARS: List[int] = [2021, 2022, 2023, 2024]


class DataDownloader:
    """
    A class used to download match and player data in JSON format
    for a specific competition and year.

    Attributes
    ----------
    selection : str
        The competition name (e.g., 'HOSTPLUS')
    year : int
        The year of the data (e.g., 2023)
    base_path : str
        Local directory to store downloaded data
    directory_path : str
        Full path to save files for the given selection and year
    base_url : str
        Remote base URL for fetching data files
    data_functions : list
        List of methods that return filenames to download
    """

    def __init__(self, selection: str, year: int, base_path: str = "./../data/") -> None:
        """
        Initialize the downloader for a specific competition and year.

        Parameters
        ----------
        selection : str
            Name of the competition
        year : int
            Year of the dataset
        base_path : str, optional
            Path to save downloaded files (default is "./../data/")
        """
        self.selection: str = selection
        self.year: int = year
        self.base_path: str = base_path
        self.directory_path: str = os.path.join(base_path, selection, str(year))
        self.base_url: str = f"{EV.DATA_WEBSITE}{selection}/{year}/"
        self.data_functions: List[Callable[[], str]] = [
            self.get_match_data,
            self.get_detailed_match_data,
            self.get_player_data
        ]

    def get_match_data(self) -> str:
        """
        Get the filename for general match data.

        Returns
        -------
        str
            Filename for match data
        """
        return f"{self.selection}_data_{self.year}.json"

    def get_detailed_match_data(self) -> str:
        """
        Get the filename for detailed match data.

        Returns
        -------
        str
            Filename for detailed match data
        """
        return f"{self.selection}_detailed_match_data_{self.year}.json"

    def get_player_data(self) -> str:
        """
        Get the filename for player statistics data.

        Returns
        -------
        str
            Filename for player statistics
        """
        return f"{self.selection}_player_statistics_{self.year}.json"

    def ensure_directory(self) -> None:
        """
        Ensure the target directory exists; if not, create it.
        """
        os.makedirs(self.directory_path, exist_ok=True)

    def download_all(self) -> None:
        """
        Download all data files (match, detailed match, player stats)
        for the specified selection and year. Skips existing files.
        """
        self.ensure_directory()

        for func in self.data_functions:
            filename: str = func()
            file_url: str = self.base_url + filename
            file_path: str = os.path.join(self.directory_path, filename)

            if os.path.exists(file_path):
                print(f"File already exists, skipping: {file_path}")
                continue

            response = requests.get(file_url)
            if response.status_code == 200:
                try:
                    data = response.json()
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    print(f"Downloaded and saved: {file_path}")
                except ValueError:
                    print(f"Failed to parse JSON from: {file_url}")
            else:
                print(f"Failed to download file: {file_url} — Status code: {response.status_code}")


# Execute downloads for all configured selection types and years
if __name__ == "__main__":
    for selection in SELECTION_TYPE:
        for year in YEARS:
            downloader = DataDownloader(selection, year)
            downloader.download_all()
