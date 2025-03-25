# NRL Machine Learning Models, Data Analytics and Data Scraper

⚠️ This library is still a Work-In-Progress. Feel free to help out by adding to the repository. ⚠️
## Description
This project is a webscraper for NRL data, and provides a TensorFlow machine learning model for NRL related predictions. 

## How to Use
Primarily use this code for Scraping at the moment. The prediction models are still a work in progress and all over the place. 
**Go to [Scraping](./scraping/README.md) for information on how to download the data manually or on how to download the entire dataset easily.**

## Data
All data for this project is hosted on [this website](https://nrlpredictions.net/sport).
I personally host this website with all data being stored in a S3 instance. 

The following data is available:
* NRL : 2001 - 2024 (you can run the scraper to get 2025 data)
* NRLW: 2022 - 2024
* KNOCKON: 2022 - 2024
* HOSTPLUS: 2022 - 2024


### 📂 Available Data Files

| Data Type                                   | Description                                                                 |
|---------------------------------------------|-----------------------------------------------------------------------------|
| **📊 Detailed Match Data**           | In-depth statistics for each match, including team performance metrics and match events. |
| **📊 General Match Data**    | Match data for every game from the selected years. |
| **👤 Player Statistics**             | Individual player performance data, including tries, tackles, run meters, and more.  |

## ⚠️ **Important Note**
- **Player data requires match data** to be retrieved first.
- Data is regularly updated and stored in a centralised location.


You can see player  data on the website, by waiting for the NRL Player Static Viewer to show (after selecting a year, type and Player Statics).

### Player Statistics

### Match Data
<details>
<summary>Match Data JSON Schema</summary>

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "NRL": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "2024": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "1": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "Details": {
                        "type": "string"
                      },
                      "Date": {
                        "type": "string"
                      },
                      "Home": {
                        "type": "string"
                      },
                      "Home_Score": {
                        "type": "string"
                      },
                      "Away": {
                        "type": "string"
                      },
                      "Away_Score": {
                        "type": "string"
                      },
                      "Venue": {
                        "type": "string"
                      }
                    },
                    "required": [
                      "Details",
                      "Date",
                      "Home",
                      "Home_Score",
                      "Away",
                      "Away_Score",
                      "Venue"
                    ]
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

</details>



### Detailed Match Data



## Workspace
This code is updated on Jupyter Notebooks (ipynb) and default python (py) files. 



## Table of Contents
- [NRL Machine Learning Models, Data Analytics and Data Scraper](#nrl-machine-learning-models-data-analytics-and-data-scraper)
  - [Description](#description)
  - [How to Use](#how-to-use)
  - [Data](#data)
    - [📂 Available Data Files](#-available-data-files)
  - [⚠️ **Important Note**](#️-important-note)
    - [Player Statistics](#player-statistics)
    - [Match Data](#match-data)
    - [Detailed Match Data](#detailed-match-data)
  - [Workspace](#workspace)
  - [Table of Contents](#table-of-contents)
  - [Web Scraping](#web-scraping)
  - [Machine Learning](#machine-learning)
  - [Web Scraping](#web-scraping-1)
  - [Visualisations](#visualisations)
  - [Conveters](#conveters)
  - [Installation](#installation)
  - [Future Tasks](#future-tasks)
  - [Help](#help)


## Web Scraping
This project utilizes Selenium/Requests for web scraping NRL data from the NRL website. Currently, I manually perform this task weekly with limited plans for automation at present. This code is located in: 
`/scraping/`




## Machine Learning 
This code is located in 
`/predictions/`
There are **two** different machine learning models:
* Match based: Uses match statistics to form the final result. This project requires furthur optimisation. 
* Player and Match based: Uses player statistics to form the final result. This project is currently WIP (however it provides code on how to manipulate the player data). 

## Web Scraping
This project utilizes Selenium for web scraping NRL data from the NRL website. Currently, I manually perform this task weekly with limited plans for automation at present. This code is located in: 
`/scraping/`

## Visualisations
Ways to Display the data are located in: 
`/visualisations/`


## Conveters
JSON is the default format for all code. Conversions tools have been generated to assist those who need .txt or .csv formats. These are located in: 
`/converters/`

## Installation
* Download the required data from the above website and place it into the `/data/` folder.
* Install the `requirements.txt` file 
* Run the Jupyter notebook located in `/predictions/`

## Future Tasks 
* Update the machine learning model to work with 2024 data
* Update the website to display prediction results
* Clean up all the code
* Optimise the current machine learning model 
* Update requirements.txt
* Provide a more descriptive README
* NRLW data
* Anytime Try Scorer Probability model
* Try Location Data
* ~~Team Stats - All Runs, All Run Metres, Post Contact Metres, Line Breaks, Tackle Breaks, Average Set Distance, Kick Return Metres, Average Play the Ball Speed, Offloads, Receipts, Total Passes, Dummy Passes, Kicks, Kicking Metres, Forced Drop Outs, Kick Defusal, Bombs, Grubbers, Effective Tackle, Tackles Made, Missed Tackles, Intercepts, Ineffective Tackles, Errors, Penalities Conceded, Ruck Infringements, On Reports, Interchanges Used~~
* Replicate https://wicky.ai/content/analytics/predictive-analytics-applied-to-rugby-league-looking-at-try-scorers-in-the-nrl/ 
* Provide a text export 

## Help 
I intend for this project to be open source, so help is always handy!
