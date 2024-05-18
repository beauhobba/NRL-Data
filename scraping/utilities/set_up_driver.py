"""
Module to set up Chrome Web Driver for Scalping.

This module provides a function to set up the Chrome Web Driver with specific options
for automated web scraping tasks related to Scalping.
"""

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chromedriver_autoinstaller.install()


def set_up_driver():
    """Set up the Chrome Web Driver for Scalping.

    This function sets up the Chrome Web Driver with specified options.
    
    :return: WebDriver object for Chrome
    """
    options = Options()
    # Ignore annoying messages from the NRL website 
    options.add_argument('--ignore-certificate-errors')
    
    # Run Selenium in headless mode
    options.add_argument('--headless')
    options.add_argument('log-level=3')
    
    # Exclude logging to assist with errors caused by NRL website 
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(options=options)
    return driver
