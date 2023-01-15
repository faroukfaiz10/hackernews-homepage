from datetime import datetime, timedelta

class Post:
    def __init__(self, title: str, url: str, score: int, date: datetime):
        self.title = title
        self.url = url
        self.score = score
        self.date = date

    """
        Warning: Sometimes, date is not correct. E.g.
        Date is "2023-01-14T08:52:23" when queried on 2023-01-15T20:11:23 but shows "1 hour ago".
        Assuming the Date is the one that's wrong because of number of the low score (6).
    """
    def is_posted_in_last_day(self):
        now = datetime.now()
        diff = now - self.date
        return diff > timedelta(days=1)

    def __str__(self) -> str:
        if self.score == -1:
            return f"NOT_SCORED - {self.title} - {self.url}"

        return f"{self.score} - {self.title} - {self.url}"