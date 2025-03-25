"""
This script fetches NRL  match data for the selected year and saves it to a JSON file
"""

# Imports
from utilities.get_nrl_data import get_nrl_data
import json
import sys
sys.path.append('..')
import ENVIRONMENT_VARIABLES as EV
import os


def match_data_select(SELECT_YEAR, SELECT_ROUNDS, SELECTION_TYPE):
    """
    Fetches NRL match data for a selected year and saves it to a JSON file.
    """
    try:
        COMPETITION_TYPE = EV.COMPETITION[SELECTION_TYPE]
    except (TypeError, KeyError):
        print(f"Unknown Competition Type: {SELECTION_TYPE}")
        return

    print(f"Fetching data for {SELECTION_TYPE} {SELECT_YEAR}...")

    match_json_datas = []
    for year in [SELECT_YEAR]:
        year_json_data = []
        for round_nu in range(1, SELECT_ROUNDS + 1):
            try:
                match_json = get_nrl_data(round_nu, year, COMPETITION_TYPE)
                year_json_data.append(match_json)
            except Exception as ex:
                print(f"Error fetching round {round_nu}: {ex}")
        match_json_datas.append({f"{year}": year_json_data})

    overall_data = {f"{SELECTION_TYPE}": match_json_datas}

    directory_path = os.path.abspath(f"../data/{SELECTION_TYPE}/{SELECT_YEAR}/")
    os.makedirs(directory_path, exist_ok=True)

    file_path = os.path.join(directory_path, f"{SELECTION_TYPE}_data_{SELECT_YEAR}.json")
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(overall_data, file, ensure_ascii=False, separators=(',', ':'))
        print(f"Saved match data to: {file_path}")
    except Exception as e:
        print(f"Error writing file: {e}")
