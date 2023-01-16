import requests
from bs4 import BeautifulSoup
from post import Post
from typing import Any

URL = "https://news.ycombinator.com/"
NUM_NEWS_PER_PAGE = 30
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
table = soup.find_all('table')[2]
rows = table.find_all('tr')


def get_age_in_hours(age: str) -> int:
    """Parses age and returns value in hours. 
    
    Age examples:
        - 1 hour ago
        - 2 hours ago
        - 12 minutes ago
    """
    time_unit = age.split(" ")[1]
    if time_unit == "minutes":
        return 1
    if time_unit == "hour":
        return 2
    if time_unit == "hours":
        return int(age.split(" ")[0]) + 1
    raise ValueError(f"Unsupported time_unit in age: {age}")

def format_url(link: str) -> str:
    if link.startswith("item?id="):
        # URLs to YC pages are relative
        return f"https://news.ycombinator.com/{link}"
    return link


def parse_post(rows: Any, index: int) -> Post: # TODO: Better typing for rows ?
    first_row = rows[index * 3]

    link = first_row.find_all('td')[2].a
    title = link.text
    url = format_url(link['href'])

    second_row = rows[index * 3 + 1]

    score_span = second_row.find('span', class_='score')
    score = int(score_span.text.split(" ")[0]) if score_span else -1

    age = second_row.find('span', class_='age').a.text
    age_in_hours = get_age_in_hours(age)
        
    return Post(title, url, score, age_in_hours)
    
posts = [parse_post(rows, i) for i in range(NUM_NEWS_PER_PAGE)]
posts_without_score = list(filter(lambda p: p.score == -1, posts))
posts.sort(key=Post.get_normalized_score, reverse= True)

if len(posts_without_score):
    print("Posts without score:")
    print(*posts_without_score, sep="\n")
    print("\nPosts with score:")

print(*posts[:10], sep="\n")