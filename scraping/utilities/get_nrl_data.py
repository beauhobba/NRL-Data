"""
Webscraper for finding NRL data related to team statistics
"""
from bs4 import BeautifulSoup
from set_up_driver import set_up_driver



def get_nrl_data(round=21, year=2023):
    url = f"https://www.nrl.com/draw/?competition=111&round={round}&season={year}"
    print(url)
    # Webscrape the NRL WEBSITE
    driver = set_up_driver() 
    page_source = driver.page_source

    driver.quit()

    # get the goodies
    soup = BeautifulSoup(page_source, "html.parser")

    # Get the NRL data box
    match_elements = soup.find_all(
        "div", class_="match o-rounded-box o-shadowed-box")

    # name of html elements to poach from the data to get the nrl specific attributes
    find_data = ["h3", "p", "p", "div", "p", "div", "p"]
    class_data = ["u-visually-hidden", "match-header__title", "match-team__name--home",
                  "match-team__score--home", "match-team__name--away", "match-team__score--away", "match-venue o-text"]

    # Extract all the useful game data
    matches_json = []
    for match_element in match_elements:
        match_details, match_date, home_team, home_score, away_team, away_score, venue = [match_element.find(
            html_val, class_=class_val).text.strip() for html_val, class_val in zip(find_data, class_data)]

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
