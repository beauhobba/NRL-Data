import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json

def get_nrl_data(round=21):
    url = f"https://www.nrl.com/draw/?competition=111&round={round}&season=2023"  

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

    # Extract all the useful game data 
    matches_json = []
    for match_element in match_elements:
        match_details = match_element.find("h3", class_="u-visually-hidden").text.strip()
        match_date = match_element.find("p", class_="match-header__title").text.strip()
        home_team = match_element.find("p", class_="match-team__name--home").text.strip()
        home_score = match_element.find("div", class_="match-team__score--home").text.strip()
        away_team = match_element.find("p", class_="match-team__name--away").text.strip()
        away_score = match_element.find("div", class_="match-team__score--away").text.strip()
        venue = match_element.find("p", class_="match-venue o-text").text.strip()

        match = {
            "Details": match_details.replace("Match", ""),
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
    for round_nu in range(1, 22):  
        match_json = get_nrl_data(round_nu)
        match_json_datas.append(match_json)
    
    overall_data = {
                "NRL": match_json_datas
            }
    overall_data_json = json.dumps(overall_data, indent=4)
    
    with open("nrl_data.json", "w") as file:
        file.write(overall_data_json)
