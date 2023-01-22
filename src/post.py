from dataclasses import dataclass

@dataclass
class Post:
    title: str
    url: str
    comments_url: str
    score: int
    age_in_hours: int

    def get_normalized_score(self) -> int:
        return int(self.score / (self.age_in_hours + 1))

    def __str__(self) -> str:
        if self.score == -1:
            return f"NOT_SCORED - {self.title} - {self.url}"
        normalized_score = self.get_normalized_score()
        base = f"{normalized_score} - {self.score} - {self.title} - {self.url}"
        return f"{base} - {self.comments_url}" if self.comments_url != ""  else base