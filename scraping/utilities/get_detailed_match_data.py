"""
Optimized Web Scraper for Finding NRL Team Statistics
"""

from bs4 import BeautifulSoup
from utilities.set_up_driver import set_up_driver
import sys

sys.path.append("..")
import ENVIRONMENT_VARIABLES as EV

# Default statistics with missing values set to -1
BARS_DATA = {
    'time_in_possession': -1, 'all_runs': -1, 'all_run_metres': -1, 'post_contact_metres': -1,
    'line_breaks': -1, 'tackle_breaks': -1, 'average_set_distance': -1, 'kick_return_metres': -1,
    'offloads': -1, 'receipts': -1, 'total_passes': -1, 'dummy_passes': -1, 'kicks': -1, 'kicking_metres': -1,
    'forced_drop_outs': -1, 'bombs': -1, 'grubbers': -1, 'tackles_made': -1, 'missed_tackles': -1,
    'intercepts': -1, 'ineffective_tackles': -1, 'errors': -1, 'penalties_conceded': -1, 'ruck_infringements': -1,
    'inside_10_metres': -1, 'interchanges_used': -1
}

DONUT_DATA = {
    'Completion Rate': -1, 'Average_Play_Ball_Speed': -1,
    'Kick_Defusal': -1, 'Effective_Tackle': -1
}

DONUT_DATA_2 = {
    'tries': -1, 'conversions': -1, 'penalty_goals': -1, 'sin_bins': -1,
    '1_point_field_goals': -1, '2_point_field_goals': -1, 'half_time': -1
}

DONUT_DATA_2_WORDS = [
    'TRIES', 'CONVERSIONS', 'PENALTY GOALS', 'SIN BINS',
    '1 POINT FIELD GOALS', '2 POINT FIELD GOALS', 'HALF TIME'
]


def get_detailed_nrl_data(round: int, year: int, home_team: str, away_team: str, driver=None, nrl_website=EV.NRL_WEBSITE):
    home_team, away_team = [x.replace(" ", "-") for x in [home_team, away_team]]

    url = f"{nrl_website}{year}/round-{round}/{home_team}-v-{away_team}/"
    print(f"Fetching data: {url}")

    # Webscrape the NRL website
    if driver is None:
        driver = set_up_driver()  # Only create a new driver if one isn't provided
    
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Initialize match data structures
    home_bars, away_bars = BARS_DATA.copy(), BARS_DATA.copy()
    home_donut, away_donut = DONUT_DATA.copy(), DONUT_DATA.copy()
    home_game_stats, away_game_stats = DONUT_DATA_2.copy(), DONUT_DATA_2.copy()
    
    # **Extract Team Possession**
    try:
        home_possession = soup.find('p', class_='match-centre-card-donut__value--home').text.strip()
        away_possession = soup.find('p', class_='match-centre-card-donut__value--away').text.strip()
    except AttributeError:
        home_possession, away_possession = None, None
        print("Error: Missing possession data.")

    # **Extract Bar Statistics (Team Stats)**
    def extract_bars(stat_list, bars_dict):
        for item, bar_name in zip(stat_list, bars_dict.keys()):
            bars_dict[bar_name] = item.get_text(strip=True)

    try:
        extract_bars(soup.find_all('dd', class_="stats-bar-chart__label--home"), home_bars)
        extract_bars(soup.find_all('dd', class_="stats-bar-chart__label--away"), away_bars)
    except Exception:
        print("Error: Issue extracting bar statistics.")

    # **Extract Donut Statistics**
    try:
        elements = soup.find_all("p", class_="donut-chart-stat__value")
        numbers = [el.get_text(strip=True) for el in elements]
        home_donut.update(dict(zip(home_donut.keys(), numbers[::2])))
        away_donut.update(dict(zip(away_donut.keys(), numbers[1::2])))
    except Exception:
        print("Error: Issue extracting donut statistics.")

    # **Extract Try Scorers & Times**
    def extract_try_scorers(team_class):
        try:
            tries = soup.find("ul", class_=team_class).find_all("li")
            names, times = zip(*[(t.get_text(strip=True).rsplit(" ", 1)) for t in tries])
            return list(names), list(times)
        except (AttributeError, ValueError):
            return [], []

    home_try_names, home_try_minutes = extract_try_scorers("match-centre-summary-group__list--home")
    away_try_names, away_try_minutes = extract_try_scorers("match-centre-summary-group__list--away")

    # **Determine First Try Scorer**
    def determine_first_scorer():
        if not home_try_minutes and not away_try_minutes:
            return None, None, None
        elif not away_try_minutes or (home_try_minutes and home_try_minutes[0] < away_try_minutes[0]):
            return home_try_names[0], home_try_minutes[0], home_team
        else:
            return away_try_names[0], away_try_minutes[0], away_team

    overall_first_try_scorer, overall_first_try_minute, overall_first_scorer_team = determine_first_scorer()

    # **Check Missing Data for DONUT_DATA_2**
    span_elements = {span.text.strip().upper() for span in soup.find_all('span', class_='match-centre-summary-group__name')}
    for word in DONUT_DATA_2_WORDS:
        if word not in span_elements:
            DONUT_DATA_2[word.lower().replace(" ", "_")] = -1

    # **Extract Match Summary Data**
    try:
        stats = [el.span.get_text(strip=True) for el in soup.find_all("span", class_="match-centre-summary-group__value")]
        home_game_stats.update(dict(zip(home_game_stats.keys(), stats[::2])))
        away_game_stats.update(dict(zip(away_game_stats.keys(), stats[1::2])))
    except Exception:
        print("Error: Issue extracting match summary statistics.")

    # **Extract Referee Data**
    try:
        refs = soup.find_all("a", class_="card-team-mate")
        ref_names = [r.find("h3", class_="card-team-mate__name").get_text(strip=True) for r in refs]
        ref_positions = [r.find("p", class_="card-team-mate__position").get_text(strip=True) for r in refs]
        main_ref_name = ref_names[0] if ref_names else None
    except Exception:
        ref_names, ref_positions, main_ref_name = [], [], None
        print("Error: Issue extracting referee data.")

    # **Extract Ground & Weather Conditions**
    ground_condition, weather_condition = None, None
    try:
        conditions = {p.get_text(strip=True).split(":")[0].strip(): p.span.get_text(strip=True) for p in soup.find_all("p", class_="match-weather__text")}
        ground_condition = conditions.get("Ground Conditions", None)
        weather_condition = conditions.get("Weather", None)
    except Exception:
        print("Error: Issue extracting weather/ground conditions.")

    # **Prepare Final Data Structure**
    match_data = {
        'overall_first_try_scorer': overall_first_try_scorer,
        'overall_first_try_minute': overall_first_try_minute,
        'overall_first_try_round': overall_first_scorer_team,
        'ref_names': ref_names, 'ref_positions': ref_positions, 'main_ref': main_ref_name,
        'ground_condition': ground_condition, 'weather_condition': weather_condition
    }

    return {'match': match_data, 'home': {**home_bars, **home_donut, **home_game_stats}, 'away': {**away_bars, **away_donut, **away_game_stats}}
