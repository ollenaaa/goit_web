from table import Table
from dataclasses import dataclass


@dataclass
class Student:
    id: int
    name: str
    groupe_id_fn: int


class StudentTable(Table):
    def __init__(self):
        super().__init__("student",
        {
            "id": "integer PRIMARY KEY autoincrement NOT NULL",
            "name": "varchar(225) unique not null",
            "groupe_id_fn": "integer"
        },
        [
            "FOREIGN KEY(groupe_id_fn) REFERENCES groupe(id)"
        ])

    def create(self, student: Student) -> int | None:
        return super().create(student.__dict__)

    def get_all(self) -> list[Student] | None:
        result = []
        rows = super.get_all()

        for i in rows:
            result.append(Student(*i))

        return result

    def update():
        pass
