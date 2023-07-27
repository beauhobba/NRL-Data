"""
Webscraper for finding NRL data related to team statistics
"""
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json

def get_nrl_data(round=21, year=2023):
    url = f"https://www.nrl.com/draw/?competition=111&round={round}&season={year}"  

    # Webscrape the shit out of the NRL website
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=ChromeDriverManager(version="114.0.5735.90").install(), options=options)
    driver.get(url)
    page_source = driver.page_source
    driver.quit()

    # get the goodies 
    soup = BeautifulSoup(page_source, "html.parser")

    # Get the NRL data box
    match_elements = soup.find_all("div", class_="match o-rounded-box o-shadowed-box")
    
    # name of html elements to poach from the data to get the nrl specific attributes
    find_data = ["h3", "p", "p", "div", "p", "div", "p"]
    class_data = ["u-visually-hidden", "match-header__title", "match-team__name--home", "match-team__score--home", "match-team__name--away", "match-team__score--away", "match-venue o-text"]
    
    # Extract all the useful game data 
    matches_json = []
    for match_element in match_elements:
        match_details, match_date, home_team, home_score, away_team, away_score, venue =  [match_element.find(html_val, class_=class_val).text.strip() for html_val, class_val in zip(find_data, class_data)]

        match = {
            "Details": match_details.replace("Match: ", ""),
            "Date": match_date,
            "Home": home_team,
            "Home_Score": home_score.replace("Scored", "").replace("points", "").strip(),
            "Away": away_team,
            "Away_Score": away_score.replace("Scored", "").replace("points", "").strip(),
            "Venue": venue.replace("Venue:", "").strip()
        }
        matches_json.append(match)
    round_data = {
                f"{round}": matches_json
            }
    return round_data

if __name__ == "__main__":
    match_json_datas = [] 
    s_year = 2023
    for year in [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2022, 2023]:
        year_json_data = [] 
        for round_nu in range(1, 22):  
            match_json = get_nrl_data(round_nu, year)
            year_json_data.append(match_json)
        year_data = {
                f"{year}": year_json_data
        }
        match_json_datas.append(year_data)
        
        
    overall_data = {
                "NRL": match_json_datas
            }
    overall_data_json = json.dumps(overall_data, indent=4)
    
    with open("nrl_data_multi_years_2.json", "w") as file:
        file.write(overall_data_json)
