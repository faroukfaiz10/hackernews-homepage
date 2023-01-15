from datetime import datetime

class Post:
    def __init__(self, title: str, url: str, score: int, date: datetime):
        self.title = title
        self.url = url
        self.score = score
        self.date = date
