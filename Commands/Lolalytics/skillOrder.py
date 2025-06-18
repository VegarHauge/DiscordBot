import requests
from bs4 import BeautifulSoup

def get_skill_order(champion):
    url = f"https://lolalytics.com/lol/{champion.lower()}/build/"
    headers = {'User-Agent': 'Mozilla/5.0'}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Find the skill order section
    skill_div = soup.find('div', attrs={'q:key': '8w_3'})
    if not skill_div:
        return []

    # Find all spans or divs that represent skill letters (e.g., "Q", "W", "E")
    skill_order = []
    for tag in skill_div.find_all(['span', 'div']):
        text = tag.get_text(strip=True)
        if text in ['Q', 'W', 'E']:
            skill_order.append(text)

    # Deduplicate in order: we only want Q > W > E once, in order of appearance
    unique_order = []
    for skill in skill_order:
        if skill not in unique_order:
            unique_order.append(skill)

    return unique_order
if __name__ == "__main__":
    # Example usage
    print(get_skill_order("Ahri"))

