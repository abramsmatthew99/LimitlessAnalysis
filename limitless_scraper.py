import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pyperclip 
from time import sleep

class Decklist:

    def __init__(self, player: str, archetype: str, deck_link : str, placement: int):
        self.player = player 
        self.archetype = archetype
        self.deck_link = deck_link
        self.placement = placement


def get_decklist_links_and_archetype(url):

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')

    lists = []
    for row in table.find_all('tr')[1:]:
        all_cells = row.find_all('td')
        #First cell contains placement, second contains name, fourth contains archetype, fifth contains list link
        placement = int(all_cells[0].text)
        name =  all_cells[1].find('a').text
        archetype = all_cells[3].find('span')["data-tooltip"]
        last_cell = all_cells[4]
        link_object = last_cell.find('a')
        if link_object:
            link = (link_object['href'])
        if link:
            lists.append(Decklist(name, archetype, link, placement))

    return lists


def create_decklist_file_from_url(deck : Decklist):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = f'https://limitlesstcg.com{deck.deck_link}'
    driver.get(url)

    button = driver.find_element(By.CLASS_NAME, "export")
    button.click()

    decklist = pyperclip.paste()
    fileName = f'{deck.player}-{deck.archetype}.txt'
    with open(fileName, 'w') as f:
        f.write(decklist)

tournament_url = "https://limitlesstcg.com/tournaments/418"  
links = get_decklist_links_and_archetype(tournament_url)
for link in links:
    create_decklist_file_from_url(link)
    sleep(1)
