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


teams = ["Broncos", "Roosters", "Wests Tigers", "Rabbitohs", "Storm", "Eels", "Raiders", "Knights", "Dragons", "Sea Eagles", "Panthers", "Sharks", "Bulldogs", "Dolphins", "Titans", "Cowboys", "Warriors"]
variables =["Year", "Win", "Versus",  "Round"]
years =  [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2022, 2023]

years_arr = {}
with open('./data/nrl_data_multi_years_2.json', 'r') as file:
    data = json.load(file)
    data = data['NRL']
    for year in years:
        years_arr[year] = data[years.index(year)][str(year)]
file.close()


years =  [2022, 2023]    
df = pd.DataFrame(columns=[f"{team} {variable}" for team in teams for variable in variables])
all_store = []
match_json_datas_2 = [] 
for year in years:
    try:
        match_json_datas = [] 
        for round in range(0, 22):
            round_data = years_arr[year][round][str(round+1)]
            round_data_ = []
            # Create an empty feature array 
            round_store = np.zeros([len(teams)*len(variables)], dtype=int)
            round_teams = []
            for game in round_data:
                h_team = game['Home'].replace(" ", "-")
                a_team = game['Away'].replace(" ", "-")
                url = f"https://www.nrl.com/draw/nrl-premiership/{year}/round-{round+1}/{h_team}-v-{a_team}/"  
                # Webscrape the shit out of the NRL website
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")
                driver = webdriver.Chrome(executable_path=ChromeDriverManager(version="114.0.5735.90").install(), options=options)
                driver.get(url)
                page_source = driver.page_source
                driver.quit()

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
                    stats_labels = [
                    "Number", "Position", "Mins Played", "Points", "Tries", "Conversions", "Conversion Attempts",
                    "Penalty Goals", "Goal Conversion Rate", "1 Point Field Goals",
                    "2 Point Field Goals", "Total Points", "All Runs", "All Run Metres",
                    "Kick Return Metres", "Post Contact Metres", "Line Breaks",
                    "Line Break Assists", "Try Assists", "Line Engaged Runs", "Tackle Breaks",
                    "Hit Ups", "Play The Ball", "Average Play The Ball Speed",
                    "Dummy Half Runs", "Dummy Half Run Metres", "One on One Steal",
                    "Offloads", "Dummy Passes", "Passes", "Receipts", "Passes To Run Ratio",
                    "Tackle Efficiency", "Tackles Made", "Missed Tackles",
                    "Ineffective Tackles", "Intercepts", "Kicks Defused", "Kicks",
                    "Kicking Metres", "Forced Drop Outs", "Bomb Kicks", "Grubbers",
                    "40/20", "20/40", "Cross Field Kicks", "Kicked Dead", "Errors",
                    "Handling Errors", "One on One Lost", "Penalties", "Ruck Infringements",
                    "Inside 10 Metres", "On Report", "Sin Bins", "Send Offs",
                    "Stint One", "Stint Two"
                    ]
                    for i, label in enumerate(stats_labels):
                        player_info[label] = statistics[i].get_text(strip=True)
                    
                    # Append player info to the list
                    players_info.append(player_info)
                    # input(players_info)
                game_data = {f"{year}-{round+1}-{h_team}-v-{a_team}": players_info}
                round_data_.append(game_data)
            round_data_op = {
                        f"{round}": round_data_
                    }
            match_json_datas.append(round_data_op)
        year_data_op = {
                    f"{year}": match_json_datas
                } 
        match_json_datas_2.append(year_data_op)
        
        
    except:
        pass
    
    
overall_data = {
        "PlayerStats": match_json_datas_2
    }
overall_data_json = json.dumps(overall_data, indent=4)

with open("./data/player_statistics_2023_2022.json", "w") as file:
    file.write(overall_data_json)

