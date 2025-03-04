"""
Webscraper for finding NRL data related to player statistics
"""

from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
from utilities.set_up_driver import set_up_driver
import sys
import os

sys.path.append('..')
import ENVIRONMENT_VARIABLES as EV

# List of variables for data extraction
variables = ["Year", "Win", "Versus", "Round"]

selected_year = 2024
selected_rounds = 1

years_overall = [selected_year]
years = [selected_year]  # Find only 2024 data for now

# Dictionary to store data for the specific year(s) of interest
years_arr = {}

# Load existing player statistics if available
player_stats_file = f"../data/player_statistics_{selected_year}.json"

if os.path.exists(player_stats_file):
    with open(player_stats_file, "r") as file:
        try:
            existing_data = json.load(file)
        except json.JSONDecodeError:
            existing_data = {"PlayerStats": []}
else:
    existing_data = {"PlayerStats": []}

# Load NRL data for matches
with open(f"../data/nrl_data_{selected_year}.json", "r") as file:
    data = json.load(file)
    data = data["NRL"]

    for year in years:
        years_arr[year] = data[years_overall.index(year)][str(year)]

df = pd.DataFrame(
    columns=[f"{team} {variable}" for team in EV.TEAMS for variable in variables]
)
all_store = []
match_json_datas_2 = []

for year in years:
    match_json_datas = []

    try:
        for round in range(0, selected_rounds):
            round_data = years_arr[year][round][str(round + 1)]
            round_data_ = []

            for game in round_data:
                h_team, a_team = [game[x].replace(" ", "-") for x in ["Home", "Away"]]
                match_key = f"{year}-{round+1}-{h_team}-v-{a_team}"

                # Skip match if already in the existing dataset
                if any(match_key in entry for entry in existing_data["PlayerStats"]):
                    print(f"Skipping existing match: {match_key}")
                    continue

                url = f"{EV.NRL_WEBSITE}{year}/round-{round+1}/{h_team}-v-{a_team}/"
                print(f"Fetching: {url}")

                # Webscrape the NRL Website
                driver = set_up_driver()
                driver.get(url)
                page_source = driver.page_source
                driver.quit()
                print("Finished Reading Website Data")

                soup = BeautifulSoup(page_source, "html.parser")

                # Find all the rows (tr elements) within the tbody
                rows = soup.find_all("tr", class_="table-tbody__tr")

                # Initialize a list to store player information
                players_info = []

                # Loop through each row and extract player data
                for row in rows:
                    player_info = {}
                    player_name_elem = row.find("a", class_="table__content-link")
                    player_name = player_name_elem.get_text(strip=True, separator=" ")

                    player_info["Name"] = player_name

                    # Extract other statistics (time, tries, etc.)
                    statistics = row.find_all("td", class_="table__cell table-tbody__td")

                    for i, label in enumerate(EV.PLAYER_LABELS):
                        try:
                            player_info[label] = statistics[i].get_text(strip=True)
                        except IndexError:
                            player_info[label] = "na"

                    players_info.append(player_info)

                # Store match data
                game_data = {match_key: players_info}
                round_data_.append(game_data)
                print(game_data)

            # Append round data
            round_data_op = {f"{round}": round_data_}
            match_json_datas.append(round_data_op)
            

    except Exception as ex:
        print(f"Error: {ex}")

    # Append yearly data
    year_data_op = {f"{year}": match_json_datas}
    match_json_datas_2.append(year_data_op)

# Merge new data with existing dataset
existing_data["PlayerStats"].extend(match_json_datas_2)

# Save updated data
with open(player_stats_file, "w") as file:
    json.dump(existing_data, file, indent=4)

print(f"Updated player statistics saved to {player_stats_file}")
