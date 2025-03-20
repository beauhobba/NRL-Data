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
    # ============================================
    # ============================================
    # Do not edit below (unless modifying code)
    # ============================================
    # ============================================

    try:
        COMPETITION_TYPE = EV.COMPETITION[SELECTION_TYPE]
    except TypeError:
        print('Unknown Competition Type')

    years = [SELECT_YEAR]

    print('Note this may take some time to run...')
    match_json_datas = []  # List to store JSON data for matches
    for year in years:
        year_json_data = []  # List to store JSON data for a particular year
        for round_nu in range(1, SELECT_ROUNDS + 1):  # Loop through 25 rounds
            try:
                # Attempt to fetch NRL data for a specific round and year
                match_json = get_nrl_data(round_nu, year, COMPETITION_TYPE)
                # Append fetched JSON to year's data list
                year_json_data.append(match_json)
            except Exception as ex:
                print(f"Error: {ex}")
        # Store year's data in a dictionary
        year_data = {
            f"{year}": year_json_data
        }
        # Append year's data to the main list
        match_json_datas.append(year_data)

    # Create overall data dictionary
    overall_data = {
        f"{SELECTION_TYPE}": match_json_datas
    }
    # Convert overall data to JSON format with indentation for better
    # readability
    overall_data_json = json.dumps(overall_data, indent=4)

    # # Write JSON data to a file
    directory_path = os.path.abspath(f"../data/{SELECTION_TYPE}/{SELECT_YEAR}/")
    file_path = os.path.join(directory_path, f"{SELECTION_TYPE}_data_{SELECT_YEAR}.json")
    try:
        with open(f"{file_path}", "w") as file:
            file.write(overall_data_json)
    except Exception as e:
        print(f"Error writing file: {e}")
            
    print('Finished Match Data Selections')