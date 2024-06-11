from config import engine
from seed import Student, Score, Lesson, Groupe, Teacher

from sqlalchemy import func, desc, and_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(f'postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}')

DBSession = sessionmaker(bind=engine)


def select_1(session):
    return session.query(Student.name, func.avg(Score.score).label('avg_score')) \
        .select_from(Score) \
        .join(Student) \
        .group_by(Student.id) \
        .order_by(desc('avg_score')) \
        .limit(5) \
        .all()


def select_2(session):
    return session.query(Student.name, func.avg(Score.score).label('avg_score')) \
        .select_from(Score) \
        .join(Student) \
        .join(Lesson) \
        .where(Lesson.id == 1) \
        .group_by(Student.id) \
        .order_by(desc('avg_score')) \
        .first()
        

def select_3(session):
    return session.query(Groupe.name, func.avg(Score.score).label('avg_score')) \
        .select_from(Groupe) \
        .join(Student) \
        .join(Score) \
        .join(Lesson) \
        .where(Lesson.id == 1) \
        .group_by(Groupe.name) \
        .all()
        

def select_4(session):
    return session.query(func.avg(Score.score).label('avg_score')).one()


def select_5(session):
    return session.query(Lesson.lesson) \
        .join(Teacher) \
        .where(Teacher.id == 2) \
        .all()


def select_6(session):
    return session.query(Student.name) \
        .join(Groupe) \
        .where(Groupe.id == 3) \
        .all()


def select_7(session):
    return session.query(Groupe.name, Student.name, Lesson.lesson, Score.score) \
        .select_from(Groupe) \
        .join(Student) \
        .join(Score) \
        .join(Lesson) \
        .where(and_(Lesson.id == 8), (Groupe.id == 1)) \
        .all()


def select_8(session):
    return session.query(Teacher.name, func.avg(Score.score).label('avg_score')) \
        .select_from(Teacher) \
        .join(Lesson) \
        .join(Score) \
        .where(Teacher.id == 4) \
        .group_by(Teacher.id) \
        .all()

def select_9(session):
    return session.query(Lesson.lesson) \
        .select_from(Student) \
        .join(Score) \
        .join(Lesson) \
        .where(Student.id == 1) \
        .distinct() \
        .all()


def select_10(session):
    return session.query(Lesson.lesson) \
        .select_from(Teacher) \
        .join(Lesson) \
        .join(Score) \
        .join(Student) \
        .where(and_(Student.id == 1), (Teacher.id == 1)) \
        .distinct() \
        .all()


if __name__ == "__main__":
    with DBSession() as session:
        result_1 = select_1(session)
        result_2 = select_2(session)
        result_3 = select_3(session)
        result_4 = select_4(session)
        result_5 = select_5(session)
        result_6 = select_6(session)
        result_7 = select_7(session)
        result_8 = select_8(session)
        result_9 = select_9(session)
        result_10 = select_10(session)

    print(f"SELECT 1\n{result_1}\n")
    print(f"SELECT 2\n{result_2}\n")
    print(f"SELECT 3\n{result_3}\n")
    print(f"SELECT 4\n{result_4}\n")
    print(f"SELECT 5\n{result_5}\n")
    print(f"SELECT 6\n{result_6}\n")
    print(f"SELECT 7\n{result_7}\n")
    print(f"SELECT 8\n{result_8}\n")
    print(f"SELECT 9\n{result_9}\n")
    print(f"SELECT 10\n{result_10}\n")