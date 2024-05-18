"""
Webscraper for finding NRL data related to team statistics
"""
from bs4 import BeautifulSoup
from utilities.set_up_driver import set_up_driver

import sys  # noqa
sys.path.append('..')  # noqa
sys.path.append('..')  # noqa
import ENVIRONMENT_VARIABLES as EV  # noqa

BARS_DATA: dict = {'time_in_possession': -1,
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

DONUT_DATA = {
        'Completion Rate': -1,
        'Average_Play_Ball_Speed': -1,
        'Kick_Defusal': -1,
        'Effective_Tackle': -1}




def get_detailed_nrl_data(
        round: int = 1,
        year: int = 2024,
        home_team: str = "sea-eagles",
        away_team: str = "rabbitohs"):
    home_team, away_team = [x.replace(" ", "-")
                            for x in [home_team, away_team]]
    
    DONUT_DATA_2 = {'tries': -1, 'conversions': -1, 'penalty_goals':-1, 'sin_bins': -1, '1_point_field_goals': -1, '2_point_field_goals': -1, 'half_time': -1}
    DONUT_DATA_2_WORDS = ['TRIES', 'CONVERSIONS', 'PENALTY GOALS',  'SIN BINS', '1 POINT FIELD GOALS','2 POINT FIELD GOALS', 'HALF TIME']



    url = f"{EV.NRL_WEBSITE}{year}/round-{round}/{home_team}-v-{away_team}/"
    print(f"{round} - {url}")

    # Webscrape the NRL WEBSITE
    driver = set_up_driver()
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page_source, "html.parser")
    

    home_possession, away_possession = None, None
    try:
        # Home possession
        home_possession = soup.find(
            'p', class_='match-centre-card-donut__value--home').text.strip()
        away_possession = soup.find(
            'p', class_='match-centre-card-donut__value--away').text.strip()
    except BaseException as BE:
        print(f"Error in home possession {BE}")

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

    home_bars, away_bars = BARS_DATA.copy(), BARS_DATA.copy()

    try:
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
    except BaseException:
        print(f"Error with home bars")

    home_donut = DONUT_DATA.copy()
    away_donut = DONUT_DATA.copy()
    


    
    
    try:
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
    except BaseException:
        print("error in donuts")

    # Initialize a list to store all names
    home_try_names_list, home_try_minute_list = [], []

    try:
        li_elements = soup.find(
            "ul", class_="match-centre-summary-group__list--home").find_all("li")

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
    except BaseException:
        print("error in home try scorers")
    home_first_try_scorer = home_try_names_list[0] if len(
        home_try_names_list) > 0 else None
    home_first_minute_scorer = home_try_minute_list[0] if len(
        home_try_minute_list) > 0 else None

    away_try_names_list = []
    away_try_minute_list = []
    try:
        li_elements = soup.find(
            "ul", class_="match-centre-summary-group__list--away").find_all("li")
        # Initialize a list to store all names

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
    except BaseException:
        print("error in away try scoers")
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


    
    # Find all span elements with the specified class
    span_elements = soup.find_all('span', class_='match-centre-summary-group__name')

    # Check if any span element contains the desired text
    for word in DONUT_DATA_2_WORDS:
        exists = any(span.text.strip().upper() == word for span in span_elements)
        if not exists:
            DONUT_DATA_2[word.lower().replace(' ', '_')] = -10
    
    home_game_stats, away_game_stats = DONUT_DATA_2.copy(), DONUT_DATA_2.copy()
    
    
    numbers = []
    try:
        span_elements = soup.find_all(
            "span", class_="match-centre-summary-group__value")
        # Loop through each <span> element and extract the number
        for span_element in span_elements:
            numbers.append(span_element.span.get_text(strip=True))
            
        filtered_home_stats = {key: value for key, value in home_game_stats.items() if value != -10}

        for k, v in zip(filtered_home_stats, numbers[::2]):
            home_game_stats[k] = v

        for k, v in zip(filtered_home_stats, numbers[1::2]):
            away_game_stats[k] = v
            
    except BaseException as Be:
        print(f"Error with match top data {Be}")
        

    main_ref_name, ref_names, ref_positions = None, [], []
    try:
        a_elements = soup.find_all("a", class_="card-team-mate")
        for a in a_elements:
            # Extract the name from <h3> element
            name = a.find("h3",
                          class_="card-team-mate__name").get_text(strip=True)
            ref_names.append(name)

            # Extract the position from <p> element
            position = a.find(
                "p", class_="card-team-mate__position").get_text(strip=True)
            ref_positions.append(position)
        main_ref_name = ref_names[0]
    except BaseException:
        print("error with ref data")

    # Initialize variables to store ground condition and weather condition
    ground_condition, weather_condition = "", ""
    try:
        # Find all <p> elements with class 'match-weather__text'
        p_elements = soup.find_all("p", class_="match-weather__text")

        # Loop through each <p> element and extract the text
        for p_element in p_elements:
            # Extract the text from the <span> element within the <p>
            condition_type = p_element.get_text(
                strip=True).split(":")[0].strip()
            condition_value = p_element.span.get_text(strip=True)

            # Check condition type and assign values accordingly
            if condition_type == "Ground Conditions":
                ground_condition = condition_value
            elif condition_type == "Weather":
                weather_condition = condition_value
    except BaseException:
        print("error with conditions")

    # Join all the data togethor into an export
    home_data = {**{'possession': home_possession,
                    'try_names': home_try_names_list,
                    'try_minutes': home_try_minute_list,
                    'first_try_scorer': home_first_try_scorer,
                    'first_try_time': home_first_minute_scorer},
                 **home_bars,
                 **home_donut,
                 **home_game_stats}

    away_data = {**{'possession': away_possession,
                    'try_names': away_try_names_list,
                    'try_minutes': away_try_minute_list,
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