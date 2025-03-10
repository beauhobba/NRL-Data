import json
import pandas as pd
import numpy as np
from utilities.get_detailed_match_data import get_detailed_nrl_data
from utilities.set_up_driver import set_up_driver
import sys

sys.path.append("..")
import ENVIRONMENT_VARIABLES as EV

# Define key variables
SELECT_YEAR = 2024
SELECT_ROUND = 27
VARIABLES = ["Year", "Win", "Defense", "Attack", "Margin", "Home", "Versus", "Round"]
JSON_FILE_PATH = f"../data/nrl_data_{SELECT_YEAR}.json"
OUTPUT_FILE_PATH = f"../data/nrl_detailed_match_data_{SELECT_YEAR}.json"

# Load NRL match data
try:
    with open(JSON_FILE_PATH, "r") as file:
        data = json.load(file)["NRL"]
except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
    print(f"Error loading JSON data: {e}")
    sys.exit(1)

# Extract data for the selected year
try:
    years_arr = {SELECT_YEAR: data[0][str(SELECT_YEAR)]}  # Use direct indexing
except IndexError as e:
    print(f"Error accessing year data: {e}")
    sys.exit(1)

# Create DataFrame with appropriate columns
df = pd.DataFrame(columns=[f"{team} {variable}" for team in EV.TEAMS for variable in VARIABLES])


# ** Function to Fetch Data for a Single Match (Using Persistent WebDriver) **
def fetch_match_data(driver, game, round_num):
    h_team, a_team = game["Home"], game["Away"]

    # Try fetching data twice before failing
    game_data = None
    for attempt in range(2):
        try:
            game_data = get_detailed_nrl_data(
                round=round_num + 1, year=SELECT_YEAR,
                home_team=h_team.lower(), away_team=a_team.lower(),
                driver=driver  # **Pass persistent WebDriver**
            )
            if "match" in game_data:
                return {f"{h_team} v {a_team}": game_data}  
        except Exception as ex:
            print(f"Attempt {attempt + 1} failed for {h_team} vs {a_team}: {ex}")

    return None 


# ** Keep Selenium WebDriver Open **
driver = set_up_driver()  # **Initialize WebDriver once**
match_json_datas = []

for round_num in range(SELECT_ROUND):
    try:
        round_data = years_arr[SELECT_YEAR][round_num][str(round_num + 1)]
        round_data_scores = []

        for game in round_data:
            match_data = fetch_match_data(driver, game, round_num)
            if match_data:
                round_data_scores.append(match_data)

        match_json_datas.append({round_num + 1: round_data_scores})

        # ** Save JSON after each round to avoid losing data **
        with open(OUTPUT_FILE_PATH, "w") as file:
            json.dump({"NRL": match_json_datas}, file, indent=4)
        print(f"✅ Round {round_num + 1} data saved.")

    except Exception as ex:
        print(f"Error processing round {round_num + 1}: {ex}")

# ** Close WebDriver after all rounds are processed **
driver.quit()
print(f"Final player statistics saved to {OUTPUT_FILE_PATH}")
