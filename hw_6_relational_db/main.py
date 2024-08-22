import sqlite3
import faker
import random
from table import Table
from student_table import StudentTable, Student
from groupe_table import GroupeTable, Groupe
from teacher_table import TeacherTable, Teacher
from score_table import ScoreTable, Score
from lesson_table import LessonTable, Lesson


database = "test.sqlite"


def number_of_elements(table_name):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]

    conn.close()
    return count


def generate_fake_groupes(table, amount, start_id):
    fake_data = faker.Faker()

    for i in range(start_id, start_id + amount):
        table.create(
            Groupe(
                i, fake_data.company()
            )
        )


def generate_fake_teachers(table, amount, start_id):
    fake_data = faker.Faker()

    for i in range(start_id, start_id + amount):
        table.create(
            Teacher(
                i, fake_data.name()
            )
        )


def generate_fake_students(table, amount, start_id):
    fake_data = faker.Faker()

    num = number_of_elements('groupe')

    for i in range(start_id, start_id + amount):
        table.create(
            Student(
                i, fake_data.name(), random.randint(1, num)
            )
        )


def generate_fake_lesson(table, amount, start_id):
    fake_data = faker.Faker()

    num = number_of_elements('teacher')
    print(num)

    for i in range(start_id, start_id + amount):
        table.create(
            Lesson(
                i, fake_data.job(), random.randint(1, num) 
            )
        )


def generate_fake_score(table, max_amount, start_id):
    fake_data = faker.Faker()

    num_stud = number_of_elements('student')
    num_less = number_of_elements('lesson')

    id = 1

    for i in range(1, num_less + 1):
        for j in range(1, num_stud + 1):
            amount = random.randint(1, max_amount)
            for k in range(0, amount):
                table.create(
                    Score(
                        id, random.randint(0, 12), fake_data.date_time(), j, i
                    )
                )
                id += 1


def select_projects(conn, sql):
    rows = None
    cur = conn.cursor()

    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()

    return rows



def main():
    with sqlite3.connect(database) as conn:
        if conn is not None:

            Table.conn = conn

            student_table = StudentTable()
            teacher_table = TeacherTable()
            groupe_table = GroupeTable()
            lesson_table = LessonTable()
            score_table = ScoreTable()

            # generate_fake_teachers(teacher_table, 2, 1)
            # generate_fake_lesson(lesson_table, 4, 1)
            # generate_fake_groupes(groupe_table, 2, 1)
            # generate_fake_students(student_table, 10, 1)
            # generate_fake_score(score_table, 2, 1)

            sql_list = ['query_1.sql', 'query_2.sql', 'query_3.sql', 'query_4.sql', 'query_5.sql', 'query_6.sql', 'query_7.sql', 'query_8.sql', 'query_9.sql', 'query_10.sql', 'query_11.sql', 'query_12.sql']

            for i in range(len(sql_list)):
                with open(f"query/{sql_list[i]}", 'r') as f:
                    sql_script = f.read()
                
                result = select_projects(conn, sql_script)
                print(f"SQL request {i + 1}\n{result}\n")
            
        else:
            print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()