from bs4 import BeautifulSoup
import requests
import html5lib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from time import sleep

from random import randint


# Define Parameters
username = "maxdeb@icloud.com"
password = "MaxLuna1"
url_sales_navigator = "https://www.linkedin.com/sales/login"
url_lead_search_victor_1 = 'https://www.linkedin.com/sales/search/people?savedSearchId=50601131&sessionId=TcZcYsm%2FT4KNXtF5Ar%2BgHw%3D%3D'
scrapeops_api_key = 'd03901b2-3693-4d44-bf16-b9d5aedf536f'



def get_headers_list(scrapeops_api_key):
    """This function retrieves a batch of the most recent headers."""
    response = requests.get(f'http://headers.scrapeops.io/v1/browser-headers?api_key={scrapeops_api_key}')
    response_json = response.json()
    return response_json.get('result', [])



def get_random_header(header_list):
    """This function configures the scraper to pick a random header from this list for each request.
    A list of optimized fake browser headers are needed to avoid blocks/bans and improve the reliability of the scraper."""
    random_index = randint(0, len(header_list) - 1)
    return header_list[random_index]



def get_driver():
    """Define Browser Options and Get URL with ChromeDrive
    Args:
        url (strigng): LinkedIn Sales Navigator URL

    Returns:
        driver: Selenium Webdriver
    """

    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument('ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)
    driver.delete_all_cookies()
    driver.maximize_window()
    return driver



def login(driver, username, password):
    """This function logs into LinkedIn Sales Navigator.
    Args:
        driver: Selenium Webdriver
        username (string): username
        password (string): password
    """

    try:
        frame = driver.find_element(By.TAG_NAME,'iframe')
        driver.switch_to.frame(frame)
        
        # Find the username and password input fields and fill them in
        username_field = driver.find_element(By.ID, 'username')
        password_field = driver.find_element(By.ID, 'password')
        username_field.send_keys(username)
        password_field.send_keys(password)
        time.sleep(1)

        # Find the login button and click it
        login_button = driver.find_element(By.CLASS_NAME, 'login__form_action_container')
        login_button.click()
        
        print("Page is ready!")

    except TimeoutException:
        print("Loading took too much time!")

    time.sleep(1)



def get_url(driver, url):
    """This function opens a given url with the provided driver."""
    print(f'Loading URL: {url}')
    driver.get(url)



def parse_html_code(url, header_list):
    """This function makes a request for a given URL and creates a BeautifulSoup object."""
    print(f'Parsing HTML code for URL: {url}')
    r = requests.get(url, headers = get_random_header(header_list))
    soup = BeautifulSoup(r.content, "html.parser")
    return soup, r


def get_names(soup):
    """This function gets the names of people on the page."""
    print(f'Finding all Names')
    # names_div = soup.find_all('div', {'class':'artdeco-entity-lockup__title.ember-view'})
    spans =  soup.select('span:contains(person)')
    print(spans)




header_list = get_headers_list(scrapeops_api_key)
print(get_random_header(header_list))
driver = get_driver()
get_url(driver, url_sales_navigator)
login(driver, username, password)
get_url(driver, url_lead_search_victor_1)
soup, r = parse_html_code(url_lead_search_victor_1, header_list)
get_names(soup)
