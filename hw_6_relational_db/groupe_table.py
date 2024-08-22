from table import Table
from dataclasses import dataclass

@dataclass
class Groupe:
    id: int
    name: str

class GroupeTable(Table):
    def __init__(self):
        super().__init__("groupe",
        {
            "id": "integer PRIMARY KEY NOT NULL",
            "name": "varchar(225) NOT NULL",
        },
        [])

    def create(self, groupe: Groupe) -> int | None:
        return super().create(groupe.__dict__)

    def get_all(self) -> list[Groupe] | None:
        result = []
        rows = super.get_all()

        for i in rows:
            result.append(Groupe(*i))

        return result
