from table import Table
from dataclasses import dataclass


@dataclass
class Teacher:
    id: int
    name: str


class TeacherTable(Table):
    def __init__(self):
        super().__init__("teacher",
        {
            "id": "integer PRIMARY KEY NOT NULL",
            "name": "varchar(225) NOT NULL"
        },
        [])

    def create(self, teacher: Teacher) -> int | None:
        return super().create(teacher.__dict__)

    def get_all(self) -> list[Teacher] | None:
        result = []
        rows = super.get_all()

        for i in rows:
            result.append(Teacher(*i))

        return result