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
# sys.path.append('..')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import ENVIRONMENT_VARIABLES as EV

# List of variables for data extraction
variables = ["Year", "Win", "Versus", "Round"]


selected_year = 2024
# selected_rounds = 27
selected_rounds = 1


years_overall = [selected_year]
years = [selected_year]  # Find only 2022 data for the time being

# Dictionary to store data for the specific year(s) of interest
years_arr = {}

# Opening the JSON file containing NRL data
with open(f'data/nrl_data_{selected_year}.json', 'r') as file:
    data = json.load(file)
    data = data['NRL']

    # Extracting data for the specified year(s)
    for year in years:
        years_arr[year] = data[years_overall.index(year)][str(year)]

# Closing the file
file.close()


# years = [2023]  # Find only 2022 data for the time being
df = pd.DataFrame(
    columns=[
        f"{team} {variable}" for team in EV.TEAMS for variable in variables])
all_store = []
match_json_datas_2 = []
for year in years:
    match_json_datas = []
    try:
        for round in range(0, selected_rounds):
            round_data = years_arr[year][round][str(round + 1)]
            round_data_ = []
            # Create an empty feature array
            round_store = np.zeros([len(EV.TEAMS) * len(variables)], dtype=int)
            round_teams = []

            for game in round_data:
                h_team, a_team = [game[x].replace(
                    " ", "-") for x in ['Home', 'Away']]
                url = f"{EV.NRL_WEBSITE}{year}/round-{round+1}/{h_team}-v-{a_team}/"

                print(url)

                # Webscrape the NRL Website
                driver = set_up_driver()
                driver.get(url)
                page_source = driver.page_source
                driver.quit()
                print('Finished Reading Website Data')

                soup = BeautifulSoup(page_source, "html.parser")


                # Initialize a list to store player information
                players_info = []

                # Find all statistic tables
                # These are table elements but need to ignore the duplicate table with aria-hidden=true
                tables = soup.select('table.table:not([aria-hidden="true"])')

                # Process each table
                for table in tables:
                    # Find the team name from the table caption
                    team_name = table.find("caption").get_text(strip=True, separator=' ').replace(" Player Stats", "")
                    
                    # Get player rows for this team
                    rows = table.find_all("tr", class_="table-tbody__tr")

                    # Loop through each row and extract player data
                    for row in rows:
                        player_info = {}

                        # Extract player name
                        player_name_elem = row.find(
                            "a", class_="table__content-link")
                        player_name = player_name_elem.get_text(
                            strip=True, separator=' ')

                        player_info["Name"] = player_name
                        player_info["Team"] = team_name

                        # Extract other statistics (time, tries, etc.)
                        statistics = row.find_all(
                            "td", class_="table__cell table-tbody__td")

                        for i, label in enumerate(EV.PLAYER_LABELS):
                            try:
                                player_info[label] = statistics[i].get_text(
                                    strip=True)
                            except BaseException:
                                player_info[label] = "na"

                        # Append player info to the list
                        players_info.append(player_info)
                        # input(players_info)
                    game_data = {
                        f"{year}-{round+1}-{h_team}-v-{a_team}": players_info}
                    round_data_.append(game_data)
            round_data_op = {
                f"{round}": round_data_
            }
            match_json_datas.append(round_data_op)
    except Exception as ex:
        print(f"Error: {ex}")
    year_data_op = {
        f"{year}": match_json_datas
    }
    match_json_datas_2.append(year_data_op)


overall_data = {
    "PlayerStats": match_json_datas_2
}

overall_data_json = json.dumps(overall_data, indent=4)


with open("../data/player_statistics_{selected_year}.json", "w") as file:
    file.write(overall_data_json)
