import sqlite3
import logging
import typing

column_name = str
column_type = str

class Table:
    conn: sqlite3.Connection = None

    def __init__(self, table_name: str, columns: dict[column_name, column_type], constrains: list[str]) -> None:
        self.table_name = table_name
        self.columns = columns
        self.constrains = constrains

        full_columns = [f"{key} {val}" for key, val in columns.items()]
        full_columns.extend(constrains)

        temp = (", ").join(full_columns)

        sql_request = f"CREATE TABLE IF NOT EXISTS {table_name} ({temp});"

        logging.debug(sql_request)

        try:
            c = self.conn.cursor()
            c.execute(sql_request)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            c.close()

    def create(self, obj: dict) -> int | None:
        table_columns = (",").join(self.columns.keys())
        table_questions = (",").join("?" for _ in self.columns.keys())

        sql_request = f"INSERT INTO {self.table_name}({table_columns}) VALUES({table_questions})"
        
        logging.debug(sql_request)

        c = self.conn.cursor()

        try:
            c.execute(sql_request, list(obj.values()))
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            c.close()

    def get_all(self) -> list[typing.Iterable[typing.Any]] | None:
        rows = None
        cur = self.conn.cursor()
        
        sql_request = f"SELECT * FROM {self.table_name}"

        try:
            cur.execute(sql_request)
            rows = cur.fetchall()
        except sqlite3.Error as e:
            print(e)
        finally:
            cur.close()
        
        return rows

