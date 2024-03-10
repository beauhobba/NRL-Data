# NRL Machine Learning Models and Data Scraper

## Description
This project is a webscraper for NRL data, and provides a TensorFlow machine learning model for NRL related predictions. 


## Data
All data for this project is hosted on [this website](nrlpredictions.com).
I personally host this website with all data being stored on a S3 instance. 

## Table of Contents
- [NRL Machine Learning Models and Data Scraper](#nrl-machine-learning-models-and-data-scraper)
  - [Description](#description)
  - [Data](#data)
  - [Table of Contents](#table-of-contents)
  - [Web Scraping](#web-scraping)
  - [Machine Learning](#machine-learning)
  - [Installation](#installation)
  - [Future Tasks](#future-tasks)
  - [Help](#help)


## Web Scraping
This project utilizes Selenium for web scraping NRL data from the NRL website. Currently, I manually perform this task weekly with limited plans for automation at present. This code is located in: 
`/scraping/`

There are **four** different web scrapers:
* Match data 2024 - *match data for every game in 2024. Updated regularly*
* Match data 2015-2024 - *match data for every game from the select years. Data is stored on the above website.* 
* Player data 2024 - *player data for every game in 2024. Updated regularly*
* Player data 2015-2024 - *player data for every game from the select years. Data is stored on the above website. *
**_NOTE:_**  To obtain player data you need match data first. 

## Machine Learning 
This code is located in 
`/predictions/`
There are **two** different machine learning models:
* Match based: Uses match statistics to form the final result. This project requires furthur optimisation. 
* Player and Match based: Uses player statistics to form the final result. This project is currently WIP (however it provides code on how to manipulate the player data). 


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

## Help 
I intend for this project to be open source, so help is always handy!