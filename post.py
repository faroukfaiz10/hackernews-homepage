class Post:
    def __init__(self, title: str, url: str, score: int, age_in_hours: int):
        self.title = title
        self.url = url
        self.score = score
        self.age_in_hours = age_in_hours

    def __str__(self) -> str:
        if self.score == -1:
            return f"NOT_SCORED - {self.title} - {self.url}"

        return f"{self.score} - {self.title} - {self.url}"