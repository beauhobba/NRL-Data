"""
Webscraper for finding NRL data related to team statistics
"""
from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
import re

chromedriver_autoinstaller.install()


def get_nrl_data(
        round=1,
        year=2024,
        home_team="sea-eagles",
        away_team="rabbitohs"):
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

    # Home possession
    home_possession = soup.find(
        'p', class_='match-centre-card-donut__value--home').text.strip()
    away_possession = soup.find(
        'p', class_='match-centre-card-donut__value--away').text.strip()

    home_all_run_metres_list = soup.find_all(
        'dd',
        class_=[
            "stats-bar-chart__label stats-bar-chart__label--home u-font-weight-700",
            "stats-bar-chart__label stats-bar-chart__label--home"])
    away_all_run_metres_list = soup.find_all(
        'dd',
        class_=[
            "stats-bar-chart__label stats-bar-chart__label--away u-font-weight-700",
            "stats-bar-chart__label stats-bar-chart__label--away"])

    home_bars = {'time_in_possession': -1,
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

    away_bars = {'time_in_possession': -1,
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
    for item, bar_name in zip(home_all_run_metres_list, home_bars.keys()):
        # Get the text of each element and strip any whitespace
        home_all_run_metres = item.get_text(strip=True)
        # Do whatever you want with the text
        home_bars[bar_name] = home_all_run_metres

    for item, bar_name in zip(away_all_run_metres_list, away_bars.keys()):
        # Get the text of each element and strip any whitespace
        home_all_run_metres = item.get_text(strip=True)
        # Do whatever you want with the text
        away_bars[bar_name] = home_all_run_metres

    home_donut = {
        'Completion Rate': -1,
        'Average_Play_Ball_Speed': -1,
        'Kick_Defusal': -1,
        'Effective_Tackle': -1}
    away_donut = {
        'Completion Rate': -1,
        'Average_Play_Ball_Speed': -1,
        'Kick_Defusal': -1,
        'Effective_Tackle': -1}

    elements = soup.find_all("p", class_="donut-chart-stat__value")
    # Loop through each element to extract the numbers
    numbers = []
    for element in elements:
        # Extract the text from the element
        text = element.get_text()
        # Find the number in the text
        number = ''.join(filter(lambda x: x.isdigit() or x == '.', text))
        numbers.append(number)
    home_donut.update({k: v for k, v in zip(home_donut, numbers[::2])})
    away_donut.update({k: v for k, v in zip(away_donut, numbers[1::2])})

    li_elements = soup.find(
        "ul", class_="match-centre-summary-group__list--home").find_all("li")

    # Initialize a list to store all names
    home_try_names_list = []
    home_try_minute_list = []
    # Loop through each <li> element and extract the name
    for li in li_elements:
        # Extract the text and remove leading/trailing whitespace
        text = li.get_text(strip=True)
        # Split the text at the space character
        parts = text.split()
        # Join the parts except the last one (which is the number) to get the
        # name
        name = ' '.join(parts[:-1])
        # Get the last part as the number
        number = parts[-1]
        # Append name and number to their respective lists
        home_try_names_list.append(name)
        home_try_minute_list.append(number)

    home_first_try_scorer = home_try_names_list[0] if len(
        home_try_names_list) > 0 else None
    home_first_minute_scorer = home_try_minute_list[0] if len(
        home_try_minute_list) > 0 else None

    li_elements = soup.find(
        "ul", class_="match-centre-summary-group__list--away").find_all("li")
    # Initialize a list to store all names
    away_try_names_list = []
    away_try_minute_list = []

    # Loop through each <li> element and extract the name
    for li in li_elements:
        # Extract the text and remove leading/trailing whitespace
        text = li.get_text(strip=True)
        # Split the text at the space character
        parts = text.split()
        # Join the parts except the last one (which is the number) to get the
        # name
        name = ' '.join(parts[:-1])
        # Get the last part as the number
        number = parts[-1]
        # Append name and number to their respective lists
        away_try_names_list.append(name)
        away_try_minute_list.append(number)

    away_first_try_scorer = away_try_names_list[0] if len(
        away_try_names_list) > 0 else None
    away_first_minute_scorer = away_try_minute_list[0] if len(
        away_try_minute_list) > 0 else None

    overall_first_try_scorer, overall_first_try_minute, overall_first_scorer_team = None, None, None 
    if away_first_try_scorer is None and home_first_try_scorer is None:
        overall_first_try_scorer = None
    else:
        if away_first_minute_scorer is None:
            overall_first_try_scorer = home_first_try_scorer
            overall_first_try_minute = home_first_minute_scorer
            overall_first_scorer_team = home_team
        elif home_first_minute_scorer is None:
            overall_first_try_scorer = away_first_try_scorer
            overall_first_try_minute = away_first_minute_scorer
            overall_first_scorer_team = away_team
        elif away_first_minute_scorer > home_first_minute_scorer:
            overall_first_try_scorer = away_first_try_scorer
            overall_first_try_minute = away_first_minute_scorer
            overall_first_scorer_team = away_team
        else:
            overall_first_try_scorer = home_first_try_scorer
            overall_first_try_minute = home_first_minute_scorer
            overall_first_scorer_team = home_team

    home_game_stats = {'tries': -1, 'conversions': -1, 'half_time': -1}
    away_game_stats = {'tries': -1, 'conversions': -1, 'half_time': -1}

    numbers = []
    span_elements = soup.find_all(
        "span", class_="match-centre-summary-group__value")
    # Loop through each <span> element and extract the number
    for span_element in span_elements:
        numbers.append(span_element.span.get_text(strip=True))
    home_game_stats.update(
        {k: v for k, v in zip(home_game_stats, numbers[::2])})
    away_game_stats.update(
        {k: v for k, v in zip(away_game_stats, numbers[1::2])})

    main_ref_name = None
    ref_names = []
    ref_positions = []
    a_elements = soup.find_all("a", class_="card-team-mate")
    for a in a_elements:
        # Extract the name from <h3> element
        name = a.find("h3", class_="card-team-mate__name").get_text(strip=True)
        ref_names.append(name)

        # Extract the position from <p> element
        position = a.find(
            "p", class_="card-team-mate__position").get_text(strip=True)
        ref_positions.append(position)
    main_ref_name = ref_names[0]

    # Find all <p> elements with class 'match-weather__text'
    p_elements = soup.find_all("p", class_="match-weather__text")

    # Initialize variables to store ground condition and weather condition
    ground_condition = ""
    weather_condition = ""

    # Loop through each <p> element and extract the text
    for p_element in p_elements:
        # Extract the text from the <span> element within the <p>
        condition_type = p_element.get_text(strip=True).split(":")[0].strip()
        condition_value = p_element.span.get_text(strip=True)

        # Check condition type and assign values accordingly
        if condition_type == "Ground Conditions":
            ground_condition = condition_value
        elif condition_type == "Weather":
            weather_condition = condition_value

    # Join all the data togethor into an export
    home_data = {**{'possession': home_possession,
                    'try_names': home_try_names_list,
                    'try_minutes': home_try_names_list,
                    'first_try_scorer': home_first_try_scorer,
                    'first_try_time': home_first_minute_scorer},
                 **home_bars,
                 **home_donut,
                 **home_game_stats}

    away_data = {**{'possession': away_possession,
                    'try_names': away_try_names_list,
                    'try_minutes': away_try_names_list,
                    'first_try_scorer': away_first_try_scorer,
                    'first_try_time': away_first_minute_scorer},
                 **away_bars,
                 **away_donut,
                 **away_game_stats}

    match_data = {
        'overall_first_try_scorer': overall_first_try_scorer,
        'overall_first_try_minute': overall_first_try_minute,
        'overall_first_try_round': overall_first_scorer_team,
        'ref_names': ref_names,
        'ref_positions': ref_positions,
        'main_ref': main_ref_name,
        'ground_condition': ground_condition,
        'weather_condition': weather_condition
    }

    game_data = {'match': match_data,
                 'home': home_data,
                 'away': away_data}

    return game_data


gd = get_nrl_data()
