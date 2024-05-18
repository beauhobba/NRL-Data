import json
import pandas as pd
import numpy as np
from utilities.get_detailed_match_data import get_detailed_nrl_data

import sys
sys.path.append('..')
import ENVIRONMENT_VARIABLES as EV

variables = [
    "Year",
    "Win",
    "Defense",
    "Attack",
    "Margin",
    "Home",
    "Versus",
    "Round"]


select_year = 2020
select_round = 27



years = [select_year]

# Initialize an empty dictionary to store data for each year
years_arr = {}
year = select_year

with open(f"../data/nrl_data_{select_year}.json", 'r') as file:
    data = json.load(file)
    data = data['NRL']
    for year in years:
        years_arr[year] = data[years.index(year)][str(year)]
# Create a DataFrame with columns representing combinations of team and
# variable names
df = pd.DataFrame(
    columns=[
        f"{team} {variable}" for team in EV.TEAMS for variable in variables])

# Iterate over each round (assuming 26 rounds)
match_json_datas = []
for round in range(0, select_round):
    try:
        # Extract data for the current round
        round_data = years_arr[year][round][str(round + 1)]

        # Create an empty feature array
        round_store = np.zeros([len(EV.TEAMS) * len(variables)], dtype=int)
        home_teams, away_teams = [], []

        # Iterate over each game in the round data
        round_data_scores = []
        for game in round_data:
            # Extract information about the game
            h_team: str = game['Home']
            h_score: int = int(game['Home_Score'])
            a_team: str = game['Away']
            a_score: int = int(game['Away_Score'])
            try:
                game_data = get_detailed_nrl_data(
                    round=round + 1,
                    year=year,
                    home_team=h_team.lower(),
                    away_team=a_team.lower())
                game_data['match']
                data = {
                    f"{h_team} v {a_team}": game_data
                }
            except Exception as ex:
                try:
                    # Try again 
                    print(f"{ex}")
                    game_data = get_detailed_nrl_data(
                        round=round + 1,
                        year=year,
                        home_team=h_team.lower(),
                        away_team=a_team.lower())
                    game_data['match']
                    data = {
                        f"{h_team} v {a_team}": game_data
                    }
                except Exception as ex:
                    print(f"{ex}")
            round_data_scores.append(data)
        match_json_datas.append({round + 1: round_data_scores})

    except Exception as ex:
        print(ex)
overall_data = {
    "NRL": match_json_datas
}
overall_data_json = json.dumps(overall_data, indent=4)

# Write JSON data to a file
with open(f"../data/nrl_detailed_match_data_{select_year}.json", "w") as file:
    file.write(overall_data_json)
