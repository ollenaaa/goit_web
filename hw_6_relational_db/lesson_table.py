from table import Table
from dataclasses import dataclass


@dataclass
class Lesson:
    id: int
    lesson: str
    teacher_id_fn: int


class LessonTable(Table):
    def __init__(self):
        super().__init__("lesson",
        {
            "id": "integer PRIMARY KEY NOT NULL",
            "lesson": "varchar(225) NOT NULL",
            "teacher_id_fn": "intager"
        },
        [
            "FOREIGN KEY(teacher_id_fn) REFERENCES teacher(id)"
        ])

    def create(self, lesson: Lesson) -> int | None:
        return super().create(lesson.__dict__)

    def get_all(self) -> list[Lesson] | None:
        result = []
        rows = super.get_all()

        for i in rows:
            result.append(Lesson(*i))

        return result