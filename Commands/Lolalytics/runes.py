import requests
from bs4 import BeautifulSoup


def get_runes(champion):
    url = f"https://lolalytics.com/lol/{champion.lower()}/build/"
    headers = {'User-Agent': 'Mozilla/5.0'}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Locate runes section
    runes_div = soup.find('div', attrs={'q:key': 'H1_5'})
    if not runes_div:
        return []

    # Find all valid rune images: must have alt, not grayscale, not statmod
    runes_imgs = runes_div.find_all('img', alt=True)

    runes = [
        img['alt']
        for img in runes_imgs
        if 'grayscale' not in img.get('class', []) and img['alt'] != "statmod"
    ]

    return runes

if __name__ == "__main__":
    print(get_runes("Ahri"))
