"""
Webscraper for finding NRL data related to player statistics
"""

import ENVIRONMENT_VARIABLES as EV
from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import pandas as pd
import numpy as np
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from utilities.set_up_driver import set_up_driver

import sys

chromedriver_autoinstaller.install()

sys.path.append('..')

# List of variables for data extraction
variables = ["Year", "Win", "Versus", "Round"]

# List of years with overall data and the specific year(s) of interest
years_overall = [2015, 2016, 2017, 2018, 2022, 2023, 2024]
# years = [2023]  # Find only 2022 data for the time being

# Dictionary to store data for the specific year(s) of interest
years_arr = {}

# Opening the JSON file containing NRL data
with open('../data/nrl_data_multi_years.json', 'r') as file:
    data = json.load(file)
    data = data['NRL']

    # Extracting data for the specified year(s)
    for year in years:
        years_arr[year] = data[years_overall.index(year)][str(year)]

# Closing the file
file.close()


years = [2015, 2016, 2017, 2018, 2022, 2023, 2024]
# years = [2023]  # Find only 2022 data for the time being
df = pd.DataFrame(
    columns=[
        f"{team} {variable}" for team in EV.TEAMS for variable in variables])
all_store = []
match_json_datas_2 = []
for year in years:
    match_json_datas = []
    try:
        for round in range(0, 27):
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

                # Webscrape the shit out of the NRL website
                driver = set_up_driver() 
                driver.get(url)
                page_source = driver.page_source
                driver.quit()
                print('Finished Reading Website Data')

                soup = BeautifulSoup(page_source, "html.parser")

                # Find all the rows (tr elements) within the tbody
                rows = soup.find_all("tr", class_="table-tbody__tr")

                # Initialize a list to store player information
                players_info = []

                # Loop through each row and extract player data
                for row in rows:
                    player_info = {}
                    # Extract player name
                    player_name_elem = row.find(
                        "a", class_="table__content-link")
                    player_name = player_name_elem.get_text(
                        strip=True, separator=' ')

                    player_info["Name"] = player_name

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


with open("../data/player_statistics_overall.json", "w") as file:
    file.write(overall_data_json)
