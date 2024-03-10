"""
Webscraper for finding NRL data related to player statistics
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
import pandas as pd 
import numpy as np
from collections import defaultdict
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options

chromedriver_autoinstaller.install() 


import ENVIRONMENT_VARIABLES as EV 


teams = ["Broncos", "Roosters", "Wests Tigers", "Rabbitohs", "Storm", "Eels", "Raiders", "Knights", "Dragons", "Sea Eagles", "Panthers", "Sharks", "Bulldogs", "Dolphins", "Titans", "Cowboys", "Warriors"]
variables =["Year", "Win", "Versus",  "Round"]
years_overall =  [2015, 2016, 2017, 2018, 2022, 2023]
years =  [2022] 
years_arr = {}
with open('./data/nrl_data_multi_years.json', 'r') as file:
    data = json.load(file)
    data = data['NRL']
    for year in years:
        years_arr[year] = data[years_overall.index(year)][str(year)]
file.close()


print(years_arr)

years =  [2015, 2016, 2017, 2018, 2022, 2023] 
years = [2022]
df = pd.DataFrame(columns=[f"{team} {variable}" for team in EV.TEAMS for variable in variables])
all_store = []
match_json_datas_2 = [] 
for year in years:
    match_json_datas = [] 
    try:
        for round in range(0, 26):
            round_data = years_arr[year][round][str(round+1)]
            round_data_ = []
            # Create an empty feature array 
            round_store = np.zeros([len(teams)*len(variables)], dtype=int)
            round_teams = []
            
            for game in round_data:
                h_team = game['Home'].replace(" ", "-")
                a_team = game['Away'].replace(" ", "-")
                url = f"{EV.NRL_WEBSITE}{year}/round-{round+1}/{h_team}-v-{a_team}/"  

                # Webscrape the shit out of the NRL website
                options = Options()
                options.add_argument('--ignore-certificate-errors')
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                driver = webdriver.Chrome(options=options)
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
                    player_name_elem = row.find("a", class_="table__content-link")
                    player_name = player_name_elem.get_text(strip=True, separator=' ')
                    
                    
                    
                    player_info["Name"] = player_name
                    
                    # Extract other statistics (time, tries, etc.)
                    statistics = row.find_all("td", class_="table__cell table-tbody__td")

                    for i, label in enumerate(EV.PLAYER_LABELS):
                        try:
                            player_info[label] = statistics[i].get_text(strip=True)
                        except:
                            player_info[label] = "na"
                    
                    # Append player info to the list
                    players_info.append(player_info)
                    # input(players_info)
                game_data = {f"{year}-{round+1}-{h_team}-v-{a_team}": players_info}
                round_data_.append(game_data)
            round_data_op = {
                        f"{round}": round_data_
                    }
            match_json_datas.append(round_data_op)
    except Exception as ex :
        print(f"Error: {ex}")
    year_data_op = {
                f"{year}": match_json_datas
            } 
    match_json_datas_2.append(year_data_op)
    

overall_data = {
        "PlayerStats": match_json_datas_2
    }

overall_data_json = json.dumps(overall_data, indent=4)


with open("./data/player_statistics_2022.json", "w") as file:
    file.write(overall_data_json)

