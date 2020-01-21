"""
    Script that performs a google search
    for 'programming' and prints a list
    of search result tiles and sections
"""

# Libraries
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

driver = None


class Config:
    """ Holds config options for the script """

    GOOGLE_HOME_PAGE = 'https://www.google.com'
    SHOW_BROWSER = True

    # CSS Selectors
    SEARCH_INPUT_BAR = "q"
    SEARCH_RESULT_BLOCK = "srg"
    SEARCH_RESULT_HITS = "rc"
    RESULT_TITLE = "h3.LC20lb"
    RESULT_SECTION = "span.st"


def setup_driver():
    """
    Creates a driver with default
    ChromeOptions
    :return: Google Chrome webdriver
    """
    global driver
    options = Options()
    if not Config.SHOW_BROWSER:
        options.add_argument("--headless")
    driver = webdriver.Chrome('/home/testing/chromedriver_linux64/chromedriver', chrome_options=options) # Change directory to where you have the chromedriver 


def sleep(sec: int =0, mins: int = 0):
    """
    Freezes code for a given amount of time
    :param sec: seconds to sleep
    :param mins: minutes to sleep
    """
    total_time = sec + (mins * 60)
    time.sleep(total_time)


def load_website(site: str):
    """
    Takes a string url and loads the site
    using the default driver and sleeps
    for a second
    :param site: string url to go to
    :return:
    """
    driver.get(site)
    sleep(sec=1)


def perform_google_search(query: str):
    """
    Takes a string query to search on Google
    This assumes that Google webpage is loaded
    :param query: string text to search
    """
    search_input = driver.find_element_by_name(Config.SEARCH_INPUT_BAR)
    search_input.send_keys(query)
    search_input.send_keys(Keys.RETURN)
    sleep(sec=1)


def parse_search_results() -> list:
    """
    Goes through the search results on google
    and parses each of the title/sections and then
    returns a list of result tuples (title, section)
    """
    result = []

    # Look if there's a featured section text block
    featured_section_text = ''
    try:
        featured_section = driver.find_element_by_class_name('ILfuVd')
        featured_section_text = featured_section.text
    except Exception:
        pass
    
    # search_result_block = driver.find_element_by_class_name(Config.SEARCH_RESULT_BLOCK)

    # Get list of search hits
    hits = driver.find_elements_by_class_name(Config.SEARCH_RESULT_HITS)

    # Parse each search result hit
    for hit in hits:
        title = hit.find_element_by_css_selector(Config.RESULT_TITLE).text
        section = hit.find_element_by_css_selector(Config.RESULT_SECTION).text

        if featured_section_text:
            result.append((title, featured_section_text))
            featured_section_text = ''
        elif title:
            result.append((title, section))

    return result


def go_to_next_page():
    """
    Finds the next page button and clicks
    on it and waits 2 seconds for loading
    """
    next_page_button = driver.find_elements_by_class_name('pn')[-1]
    next_page_button.click()
    sleep(sec=2)


def print_results(results: list):
    """
    Takes a list of tuples (title, section)
    and print each result
    :param results: [(title, section)]
    """
    for result in results:
        print('Title: ', result[0])
        print('Section: ', result[1])
        print()


""" MAIN """

# Setup the web driver
setup_driver()

# Open up google home page
load_website(Config.GOOGLE_HOME_PAGE)

# Search for "programming"
perform_google_search("programming")

# Search for title/section (page 1)
results1 = parse_search_results()

# Navigate to page 2
go_to_next_page()

# Search for title/section (page 2)
results2 = parse_search_results()


# Combine results from both pages
combined_results = results1 + results2

# Print them
print_results(combined_results)
