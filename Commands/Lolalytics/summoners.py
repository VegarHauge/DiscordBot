import requests
from bs4 import BeautifulSoup

def get_summoner(champion):
    url = f"https://lolalytics.com/lol/{champion.lower()}/build/"
    headers = {'User-Agent': 'Mozilla/5.0'}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Find summoner spell section
    summoners_div = soup.find('div', attrs={'q:key': 'uE_3'})
    if not summoners_div:
        return []

    # Get all relevant images with alt text (summoner spells)
    summoner_imgs = summoners_div.find_all('img', alt=True)

    # Extract alt text
    summoners = [img['alt'] for img in summoner_imgs]

    # Deduplicate (e.g., Flash appears twice across pairings)
    return list(dict.fromkeys(summoners))
if __name__ == "__main__":
    print(get_summoner("darius"))
