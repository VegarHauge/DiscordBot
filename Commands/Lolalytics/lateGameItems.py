import requests
from bs4 import BeautifulSoup

def get_late_game_items(champion):
    url = f"https://lolalytics.com/lol/{champion.lower()}/build/"
    headers = {'User-Agent': 'Mozilla/5.0'}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Find all item sets that share q:key="40_4" – these are item4, item5, item6 sets
    item_divs = soup.find_all('div', attrs={'q:key': '40_4'})

    late_game_items = {
        'item4': [],
        'item5': [],
        'item6': []
    }

    for i, div in enumerate(item_divs[:3]):  # limit to first 3
        item_imgs = div.find_all('img', alt=True)
        item_names = [img['alt'] for img in item_imgs if 'item64' in img.get('src', '')]

        if i == 0:
            late_game_items['item4'] = item_names
        elif i == 1:
            late_game_items['item5'] = item_names
        elif i == 2:
            late_game_items['item6'] = item_names

    return late_game_items
if __name__ == "__main__":
    print(get_late_game_items("Ahri"))