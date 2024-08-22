from table import Table
from dataclasses import dataclass
from datetime import date


@dataclass
class Score:
    id: int
    score: float
    date: date
    student_id_fn: int
    lesson_id_fn: int


class ScoreTable(Table):
    def __init__(self):
        super().__init__("score",
        {
            "id": "INTEGER PRIMARY KEY NOT NULL",
            "score": "INTEGER CHECK(score >= 0 AND score <= 12)",
            "date": "DATE",
            "student_id_fn": "integer",
            "lesson_id_fn": "integer"
        },
        [
            "FOREIGN KEY(student_id_fn) REFERENCES student(id)",
            "FOREIGN KEY(lesson_id_fn) REFERENCES lesson(id)"
        ])

    def create(self, score: Score) -> int | None:
        return super().create(score.__dict__)

    def get_all(self) -> list[Score] | None:
        result = []
        rows = super.get_all()

        for i in rows:
            result.append(Score(*i))

        return result