import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pyperclip 


def get_decklist_links(url):

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')

    links = []
    for row in table.find_all('tr')[1:]:
        last_cell = row.find_all('td')[-1]
        link = last_cell.find('a')
        if link:
            links.append(link['href'])

    return links


def create_decklist_file_from_url(url_extension):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = f'https://limitlesstcg.com{url_extension}'
    driver.get(url)

    button = driver.find_element(By.CLASS_NAME, "export")
    button.click()

    decklist = pyperclip.paste()

    deck_id = url_extension.split("/")[-1]
    fileName = f'{deck_id}.txt'
    with open(fileName, 'w') as f:
        f.write(decklist)

tournament_url = "https://limitlesstcg.com/tournaments/418"  
links = get_decklist_links(tournament_url)
for link in links:
    create_decklist_file_from_url(link)
