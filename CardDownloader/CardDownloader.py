import requests
from collections import OrderedDict
import urllib.request
from bs4 import BeautifulSoup

def get_monoface_cards(colour_root):
    images = colour_root.find_all('img')

    cards = OrderedDict()

    for image in images:
        cards[image['alt']] = [image['src']]

    return cards

def add_dualface_cards(dual_root, cards_by_colour):
    images = dual_root.find_all('div', {'class' : 'image'})

    previous_name = ""
    current_colour = 0

    for image in images:
        front_side = image.find('div', {'class' : 'side front'})
        back_side = image.find('div', {'class' : 'side back'})

        front_image = front_side.find('img')
        back_image = back_side.find('img')

        card_name = front_image['alt']

        if previous_name != "" and previous_name > card_name:
            current_colour += 1

        cards_by_colour[current_colour][card_name] = [front_image['src'], back_image['src']]
        
        previous_name = card_name

def download_images(cards_by_colour):
    card_number = 1

    for colour in cards_by_colour:
        for card in colour:
            if len(card[1]) == 1:
                print("Hi")

def main():
    r = requests.get('https://magic.wizards.com/en/articles/archive/card-image-gallery/innistrad-midnight-hunt')
    soup = BeautifulSoup(r.content, features="html.parser")

    white_div = soup.find('div', {'id': 'divwhite'})
    blue_div = soup.find('div', {'id': 'divblue'})
    black_div = soup.find('div', {'id': 'divblack'})
    red_div = soup.find('div', {'id': 'divred'})
    green_div = soup.find('div', {'id': 'divgreen'})
    multi_div = soup.find('div', {'id': 'divmulticolored'})
    artifact_div = soup.find('div', {'id': 'divartifact'})
    land_div = soup.find('div', {'id': 'divland'})
    dual_div = soup.find('div', {'id': 'divmeld'})

    cards_by_colour = []
    cards_by_colour.append(get_monoface_cards(white_div))
    cards_by_colour.append(get_monoface_cards(blue_div))
    cards_by_colour.append(get_monoface_cards(black_div))
    cards_by_colour.append(get_monoface_cards(red_div))
    cards_by_colour.append(get_monoface_cards(green_div))
    cards_by_colour.append(get_monoface_cards(multi_div))
    cards_by_colour.append(get_monoface_cards(artifact_div))
    cards_by_colour.append(get_monoface_cards(land_div))

    add_dualface_cards(dual_div, cards_by_colour)

    print(cards_by_colour)


main()