"""
Webscraper for finding NRL data related to team statistics
"""
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
import re 

chromedriver_autoinstaller.install()


def get_nrl_data(round=1, year=2024, home_team="sea-eagles", away_team = "rabbitohs"):
    url = f"https://www.nrl.com/draw/nrl-premiership/{year}/round-{round}/{home_team}-v-{away_team}/"

    # Webscrape the NRL WEBSITE
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    page_source = driver.page_source

    driver.quit()

    # get the goodies
    soup = BeautifulSoup(page_source, "html.parser")

    # Get the NRL data box
    match_elements = soup.find_all(
        "div", class_="match o-rounded-box o-shadowed-box")

    # name of html elements to poach from the data to get the nrl specific attributes
    # find_data = ["h3", "p", "p", "div", "p", "div", "p"]
    # class_data = ["u-visually-hidden", "match-header__title", "match-team__name--home",
    #               "match-team__score--home", "match-team__name--away", "match-team__score--away", "match-venue o-text"]


    # Time in possession 
    home_time_in_possession = soup.find('dd', class_='stats-bar-chart__label--home')
    home_time_in_possession = home_time_in_possession.get_text().strip()
    
    away_time_in_possession = soup.find('dd', class_='stats-bar-chart__label--away')
    away_time_in_possession = away_time_in_possession.get_text().strip()
    
    print(f"{home_time_in_possession} {away_time_in_possession}")
    
    # Home possession 
    home_possession = soup.find('p', class_='match-centre-card-donut__value--home').text.strip()
    away_possession = soup.find('p', class_='match-centre-card-donut__value--away').text.strip()
    
    print(f"{home_possession} {away_possession}")
    
    # Completion Rate
    filtered_p_tags = soup.find_all('p', class_=["match-centre-card-donut__value match-centre-card-donut__value--footer", "match-centre-card-donut__value match-centre-card-donut__value--footer u-font-weight-500"], text=lambda text: '/' in text)
    home_completion_rate = (filtered_p_tags[0].text)
    away_completion_rate = (filtered_p_tags[1].text)
    
    
    numerator_str, denominator_str = home_completion_rate.split('/')
    home_completion_rate = float(numerator_str) / float(denominator_str)

    numerator_str, denominator_str = away_completion_rate.split('/')
    away_completion_rate = float(numerator_str) / float(denominator_str)

    print(f"{home_completion_rate} {away_completion_rate}")
    
    home_all_runs = soup.find('dd', class_="stats-bar-chart__label stats-bar-chart__label--home u-font-weight-700").get_text(strip=True)
    away_all_runs = soup.find('dd', class_="stats-bar-chart__label stats-bar-chart__label--away u-font-weight-700").get_text(strip=True)
    print(f"{home_all_runs} {away_all_runs}")
    
    
    
    home_all_run_metres_list = soup.find_all('dd', class_=["stats-bar-chart__label stats-bar-chart__label--home u-font-weight-700", "stats-bar-chart__label stats-bar-chart__label--home"])
    bars = {'time_in_possession': -1,
            'all_runs': -1,
            'all_run_metres': -1,
            'post_contact_metres': -1,
            'line_breaks': -1,
            'tackle_breaks': -1,
            'average_set_distance': -1,
            'kick_return_metres': -1,
            'offloads': -1,
            'receipts': -1,
            'total_passes': -1,
            'dummy_passes': -1,
            'kicks': -1,
            'kicking_metres': -1,
            'forced_drop_outs': -1,
            'bombs': -1,
            'grubbers': -1,
            'tackles_made': -1,
            'missed_tackles': -1,
            'intercepts': -1,
            'ineffective_tackles': -1,
            'errors': -1,
            'penalties_conceded': -1,
            'ruck_infringements': -1,
            'inside_10_metres': -1,
            'interchanges_used': -1}

    # Loop through each element
    for item, bar_name in zip(home_all_run_metres_list, bars.keys()):
        # Get the text of each element and strip any whitespace
        home_all_run_metres = item.get_text(strip=True)
        # Do whatever you want with the text
        bars[bar_name] = home_all_run_metres
        
    input(bars)
    
    
    # home_all_run_metres = soup.find('dd', class_="stats-bar-chart__label stats-bar-chart__label--home u-font-weight-700").get_text(strip=True)
    # home_all_run_metres = re.sub(r'[^\d]+', '', home_all_run_metres)
    # away_all_run_metres = soup.find('dd', class_="stats-bar-chart__label stats-bar-chart__label--away u-font-weight-700").get_text(strip=True)
    # away_all_run_metres = re.sub(r'[^\d]+', '', away_all_run_metres)
    # print(f"{home_all_run_metres} {away_all_run_metres}")
    
    
    
    
    
    
    
    
    
    
    
    
    # Extract all the useful game data
    matches_json = []
    
    
    round_data = {} 
    # for match_element in match_elements:
    #     match_details = [match_element.find(
    #         html_val, class_=class_val).text.strip() for html_val, class_val in zip(find_data, class_data)]
        
    #     input(match_details)

    #     match = {
    #         "Details": match_details.replace("Match: ", ""),
    #         # "Date": match_date,
    #         # "Home": home_team,
    #         # "Home_Score": home_score.replace("Scored", "").replace("points", "").strip(),
    #         # "Away": away_team,
    #         # "Away_Score": away_score.replace("Scored", "").replace("points", "").strip(),
    #         # "Venue": venue.replace("Venue:", "").strip()
    #     }
    #     matches_json.append(match)
    # round_data = {
    #     f"{round}": matches_json
    # }
    return round_data


get_nrl_data()