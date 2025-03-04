# Scrapers

## Overview
This script fetches and saves NRL player statistics per round for a selected year. It is optimized for fast execution using a persistent Selenium WebDriver.

## Usage

### Running the Web Scraper
Execute the following command from the `scraping` directory:
```bash
python match_data_detailed_select.py
```

### Script Functionality
1. **Loads Match Data**
   - Reads `nrl_data_YEAR.json` containing match details.
   - Extracts match information (teams, round, and year).

2. **Scrapes Player Statistics**
   - Uses Selenium WebDriver to navigate to match pages.
   - Extracts player statistics using BeautifulSoup.
   - Stores match and player data in JSON format.

3. **Saves Data**
   - Writes to `player_statistics_YEAR.json` after each round.
   - Ensures data is saved incrementally to prevent loss.

## Output Files
- `data/nrl_data_YEAR.json`: Raw match data.
- `data/player_statistics_YEAR.json`: Player statistics structured as:
  ```json
  {
      "PlayerStats": [
          {
              "YEAR": [
                  {
                      "Round": [
                          { "Match": [{"Player Name": "Stats"}] }
                      ]
                  }
              ]
          }
      ]
  }
  ```


## Notes
- Ensure `chromedriver` is properly configured.
- Modify `selected_year` and `selected_rounds` in scripts to adjust the range.
- The script may require updates if the NRL website structure changes.

For any issues, refer to console logs for debugging.

