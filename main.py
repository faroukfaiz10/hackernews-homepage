import requests
from bs4 import BeautifulSoup
from post import Post
from typing import Any

URL_PREFIX = "https://news.ycombinator.com/news?p="
NUM_NEWS_PER_PAGE = 30

def get_age_in_hours(age: str) -> int:
    """Parses age and returns value in hours. 
    
    Age examples:
        - 1 hour ago
        - 2 hours ago
        - 12 minutes ago
    """
    time_unit = age.split(" ")[1]
    if time_unit == "minutes":
        return 0
    if time_unit == "hour":
        return 1
    if time_unit == "hours":
        return int(age.split(" ")[0])
    if time_unit == "day":
        return 24
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

def print_posts(posts: 'list[Post]'):
    print(*posts, sep="\n")

def fetch_page_posts(page_index: int) -> 'list[Post]':
    page = requests.get(f"{URL_PREFIX}{page_index}")

    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find_all('table')[2]
    rows = table.find_all('tr')
    
    return [parse_post(rows, i) for i in range(NUM_NEWS_PER_PAGE)]

def main():
    posts = [fetch_page_posts(i) for i in [1, 2, 3]]
    flattened_posts = [post for page_posts in posts for post in page_posts]
    posts_without_score = list(filter(lambda p: p.score == -1, flattened_posts))
    flattened_posts.sort(key=Post.get_normalized_score, reverse= True)

    if len(posts_without_score):
        print("Posts without score:")
        print_posts(posts_without_score)
        print("\nPosts with score:")

    print_posts(flattened_posts[:10])

if __name__ == "__main__":
    main()