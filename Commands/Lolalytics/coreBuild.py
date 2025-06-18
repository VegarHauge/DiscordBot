import requests
from bs4 import BeautifulSoup

def get_core_build(champion):
    url = f"https://lolalytics.com/lol/{champion.lower()}/build/"
    headers = {'User-Agent': 'Mozilla/5.0'}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Find core build section
    core_build_div = soup.find('div', attrs={'q:key': 'g1_2'})
    if not core_build_div:
        return []

    # Get all relevant item images
    item_imgs = core_build_div.find_all('img', alt=True)

    # Extract item names
    core_items = [img['alt'] for img in item_imgs if 'item64' in img.get('src', '')]

    return core_items
if __name__ == "__main__":
    print(get_core_build("Ahri"))
