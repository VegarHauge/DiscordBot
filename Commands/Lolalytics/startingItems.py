import requests
from bs4 import BeautifulSoup

def get_starting_items(champion):
    url = f"https://lolalytics.com/lol/{champion.lower()}/build/"
    headers = {'User-Agent': 'Mozilla/5.0'}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Find the div with q:key="or_1" (starting items section)
    starting_items_div = soup.find('div', attrs={'q:key': 'or_1'})
    if not starting_items_div:
        return []

    # Find all images inside it with an alt attribute
    item_imgs = starting_items_div.find_all('img', alt=True)

    # Extract item names from alt attributes
    starting_items = [img['alt'] for img in item_imgs if 'item64' in img.get('src', '')]

    return starting_items

if __name__ == "__main__":
    print(get_starting_items("leblanc"))
