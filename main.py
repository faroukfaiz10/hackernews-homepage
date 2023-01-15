import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://news.ycombinator.com/"
NUM_NEWS_PER_PAGE = 30
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
table = soup.find_all('table')[2]
rows = table.find_all('tr')

for i in range(NUM_NEWS_PER_PAGE):
    first_row = rows[i * 3]

    link = first_row.find_all('td')[2].a
    title = link.text
    url = link['href']

    second_row = rows[i * 3 + 1]

    score = int(second_row.find('span', class_='score').text.split(" ")[0])
    age = datetime.fromisoformat(second_row.find('span', class_='age')['title'])