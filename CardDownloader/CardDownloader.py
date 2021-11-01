import requests
from bs4 import BeautifulSoup

def get_monocolour_cards(colour_root):
    images = colour_root.find_all('img')

    cards = {}

    for image in images:
        cards[image['alt']] = [image['src']]

    return cards


def main():
    r = requests.get('https://magic.wizards.com/en/articles/archive/card-image-gallery/innistrad-midnight-hunt')
    soup = BeautifulSoup(r.content, features="html.parser")

    white_div = soup.find('div', {'id': 'divwhite'})
    blue_div = soup.find('div', {'id': 'divblue'})
    black_div = soup.find('div', {'id': 'divblack'})
    red_div = soup.find('div', {'id': 'divred'})
    green_div = soup.find('div', {'id': 'divgreen'})

    white_cards = get_monocolour_cards(white_div)
    blue_cards = get_monocolour_cards(blue_div)
    black = get_monocolour_cards(black_div)
    red_cards = get_monocolour_cards(red_div)
    white_cards = get_monocolour_cards(black_div)

    blu

    print(white_cards)


main()