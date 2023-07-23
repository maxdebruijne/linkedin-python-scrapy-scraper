from bs4 import BeautifulSoup
import pandas as pd
import requests
import html5lib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import unidecode
import time
from time import sleep


# Get URL
url = "https://contao.bvkap.de/private-equity/capital-search.html"


driver = webdriver.Chrome()
actions = ActionChains(driver)
driver.maximize_window()
driver.get(url)

sleep(2)

# Accept Cookies
element = driver.execute_script("""return document.querySelector('#usercentrics-root').shadowRoot.querySelector("button[data-testid='uc-accept-all-button']")""")
element.click()

sleep(2)

# Add 20 to Transaction Volume
transaction_volume = driver.find_element(By.ID, 'ctrl_transaction')
transaction_volume.send_keys('20')
time.sleep(1)

# Click Header
driver.find_element(By.XPATH, '//*[@id="element-frm"]/div/div[2]/div/div[2]/a').click()
time.sleep(1)

# Click Filters
driver.find_element(By.XPATH, '//*[@id="opt_industry_sector_25"]').click()
driver.find_element(By.XPATH, '//*[@id="opt_geo_focus_0"]').click()
time.sleep(5)

# Press Submit
driver.find_element(By.CLASS_NAME, 'button.btn.btn-primary.w-100.send-btn').click()

#Start Scraping Company Names
page = driver.page_source
soup = BeautifulSoup(page)
company_names = [unidecode.unidecode(tag.text.lower().replace(' ', '-').replace('.', '').replace('///-','')
                                     .replace('&-', '').replace('&','').replace('(','').replace(')','')
                                     .replace('\-','').replace(',','')) for tag in soup.find_all('div', {'class': 'company-name'})]
print(company_names)

time.sleep(1)


# get all addresses
company_addresses = [tag.text for tag in soup.find_all('span', {'class': 'map'})]
print(company_addresses)

# Scrape all URLs

time.sleep(5)

all_company_information = {}

for company in company_names:
    try:
        company_url = f'https://contao.bvkap.de/the-bvk/members/mitglieder-details/user/{company}.html'
        company_dict = {}
        driver.get(company_url.replace('-.html', '.html'))

        page = driver.page_source
        soup = BeautifulSoup(page)
        try:
            company_dict['Street'] = soup.find('span', {'class', 'street'}).text
        except:
            company_dict['Street'] = ''

        try:
            company_dict['Postal Code'] = soup.find('span', {'class', 'postal'}).text
        except:
            company_dict['Postal Code'] = ''

        try:
            company_dict['City'] = soup.find('span', {'class', 'city'}).text
        except:
            company_dict['City'] = ''

        try:
            company_dict['Conact Person'] = soup.find('div', {'class':'contact-persons'}).find('div', {'class':'contact-people'}).text
        except:
            company_dict['Conact Person'] = ''

        try:
            company_dict['Phone'] = soup.find('div', {'class':'contact-phone'}).find('div', {'class':'details'}).text
        except:
            company_dict['Phone'] = ''

        try:
            company_dict['Website'] = soup.find('div', {'class':'contact-homepage'}).find_next('a').get('href')
        except:
            company_dict['Website'] = ''

        try:
            company_dict['Email'] = soup.find('div', {'class':'contact-mails'}).find_next('a').get('href')[7:]
        except:
            company_dict['Email'] = ''    

        all_company_information[company] = company_dict

        time.sleep(2)

    except Exception as e:
        print(f'Company URL Not Found: {company_url}')
        time.sleep(1)


print(all_company_information)

df = pd.DataFrame.from_dict(all_company_information).transpose()
print(df)
df.to_excel('private_equity_info.xlsx', sheet_name='PE Germany')
df.to_csv('private_equity_info.csv')