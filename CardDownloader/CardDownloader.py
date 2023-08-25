from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

import time
import os
import urllib

class Card:
    def __init__(self, name, imageUrl):
        self.name = name
        self.imageUrl = imageUrl
        
    def __str__(self):
        return self.name

def set_color(driver, color):
    color_selector = Select(driver.find_element(By.NAME, 'sort-by-color'))
    color_selector.select_by_value(color)
    
def set_set(driver, set_id):
    set_selector = Select(driver.find_element(By.NAME, 'sort-by-card-set'))
    set_selector.select_by_value(set_id)

def set_treatment(driver):
    set_selector = Select(driver.find_element(By.NAME, 'sort-by-treatment'))
    set_selector.select_by_value('traditional-foil')
    
def get_all_cards(driver):
    cards = set([])
    scroll_to_bottom(driver)
    card_elements = driver.find_elements(By.TAG_NAME, 'magic-card')
    for card_element in card_elements:
        card_name = card_element.get_attribute('name')
        if any(x.name == card_name for x in cards): continue
        image_element = card_element.find_elements(By.TAG_NAME, 'img')
        imageUrl = image_element[0].get_attribute('src')
        cards.add(Card(card_name, imageUrl))

    return cards

def scroll_to_bottom(driver):
    for i in range(100):
        driver.execute_script("window.scrollBy(0, {delta});".format(delta=100))
        time.sleep(.05)
        
def scroll_to_top(driver):
    driver.execute_script("window.scrollTo(0, 0);")

def download_cards(card_lists, colors):
    card_number = 1
    
    card_directory = "./cards"

    if not os.path.exists(card_directory):
        os.mkdir(card_directory)

    for color in colors:
        for card in sorted(card_lists[color], key=by_name):
            print(card.name)
            urllib.request.urlretrieve(card.imageUrl, f"{card_directory}/{card_number}.png")
            card_number += 1
    
def reset(driver):
    driver.refresh()
    time.sleep(1)

def by_name(card):
    return card.name.removeprefix('A ').removeprefix('The ')

def main():
    options = Options()
    options.headless = False #True
    options.add_argument("--window-size=1920,1200")
    
    service = Service(executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')

    driver = webdriver.Chrome(options=options, service=service)
    driver.get('https://magic.wizards.com/en/products/wilds-of-eldraine/card-image-gallery')
    
    colors = ['white', 'blue', 'black', 'red', 'green', 'multicolor', 'artifact', 'land']
    card_lists = {}
    
    for color in colors:
        set_set(driver, 'WOE')
        set_color(driver, color)
        card_lists[color] = get_all_cards(driver)
        reset(driver)
        
    for color in colors:
        for card in sorted(card_lists[color], key=by_name):
            print(card.name)

    ## Mystical Archive cards
    set_set(driver, 'WOT')
    for color in colors:
        set_color(driver, color)
        set_treatment(driver)
        card_lists[color].update(get_all_cards(driver))
        reset(driver)
        
    download_cards(card_lists, colors)
    

    driver.quit()

main()