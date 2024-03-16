import json
import pandas as pd
import numpy as np
from utilities.get_detailed_match_data import get_detailed_nrl_data

teams = [
    "Broncos",
    "Roosters",
    "Wests Tigers",
    "Rabbitohs",
    "Storm",
    "Eels",
    "Raiders",
    "Knights",
    "Dragons",
    "Sea Eagles",
    "Panthers",
    "Sharks",
    "Bulldogs",
    "Dolphins",
    "Titans",
    "Cowboys",
    "Warriors"]
variables = [
    "Year",
    "Win",
    "Defense",
    "Attack",
    "Margin",
    "Home",
    "Versus",
    "Round"]
years = [2023]

# Initialize an empty dictionary to store data for each year
years_arr = {}
year = 2023

with open('../data/nrl_data_2023.json', 'r') as file:
    data = json.load(file)
    data = data['NRL']
    for year in years:
        years_arr[year] = data[years.index(year)][str(year)]
# Create a DataFrame with columns representing combinations of team and
# variable names
df = pd.DataFrame(
    columns=[
        f"{team} {variable}" for team in teams for variable in variables])

# Iterate over each round (assuming 26 rounds)
match_json_datas = []
for round in range(0, 27):
    print(round)
    try:
        # Extract data for the current round
        round_data = years_arr[year][round][str(round + 1)]

        # Create an empty feature array
        round_store = np.zeros([len(teams) * len(variables)], dtype=int)
        home_teams, away_teams = [], []

        # Iterate over each game in the round data
        round_data_scores = []
        for game in round_data:
            print(game)
            # Extract information about the game
            h_team: str = game['Home']
            h_score: int = int(game['Home_Score'])
            a_team: str = game['Away']
            a_score: int = int(game['Away_Score'])
            game_data = get_detailed_nrl_data(
                round=round + 1,
                year=year,
                home_team=h_team.lower(),
                away_team=a_team.lower())
            game_data['match']
            data = {
                f"{h_team} v {a_team}": game_data
            }
            print(f"{h_team} v {a_team}")
            round_data_scores.append(data)
        match_json_datas.append({round + 1: round_data_scores})

    except Exception as ex:
        print(ex)
overall_data = {
    "NRL": match_json_datas
}
overall_data_json = json.dumps(overall_data, indent=4)

# Write JSON data to a file
with open("../data/nrl_detailed_match_data_2023.json", "w") as file:
    file.write(overall_data_json)
