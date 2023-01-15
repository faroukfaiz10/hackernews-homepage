import requests
from bs4 import BeautifulSoup
from datetime import datetime
from post import Post
from typing import Any

URL = "https://news.ycombinator.com/"
NUM_NEWS_PER_PAGE = 30
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
table = soup.find_all('table')[2]
rows = table.find_all('tr')

def parse_post(rows: Any, index: int) -> Post: # TODO: Better typing for rows ?
    first_row = rows[index * 3]

    link = first_row.find_all('td')[2].a
    title = link.text
    url = link['href']

    second_row = rows[index * 3 + 1]

    score_span = second_row.find('span', class_='score')
    score = int(score_span.text.split(" ")[0]) if score_span else -1

    date = datetime.fromisoformat(second_row.find('span', class_='age')['title'])
    return Post(title, url, score, date)
    
posts = [parse_post(rows, i) for i in range(NUM_NEWS_PER_PAGE)]
posts_without_score = list(filter(lambda p: p.score == -1, posts))
posts.sort(key=lambda p: p.score, reverse= True)

if len(posts_without_score):
    print("Posts without score:")
    print(*posts_without_score, sep="\n")
    print("\nPosts with score:")

print(*posts[:10], sep="\n")