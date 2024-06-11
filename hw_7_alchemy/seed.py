import faker
import datetime
import sqlalchemy
import random

from sqlalchemy import create_engine, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from sqlalchemy.orm import declarative_base

import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(f'postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}')

DBSession = sessionmaker(bind=engine)
Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    groupe_id: Mapped[int] = mapped_column(ForeignKey('groupes.id', ondelete="CASCADE"))


class Groupe(Base):
    __tablename__ = 'groupes'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


class Lesson(Base):
    __tablename__ = 'lessons'

    id: Mapped[int] = mapped_column(primary_key=True)
    lesson: Mapped[str] = mapped_column(String, nullable=False)
    teacher_id : Mapped[int] = mapped_column(ForeignKey('teachers.id', ondelete="CASCADE"))


class Score(Base):
    __tablename__ = 'scores'

    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id', ondelete="CASCADE"))
    lesson_id: Mapped[int] = mapped_column(ForeignKey('lessons.id', ondelete="CASCADE"))


def init_db():
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)

    fake_data = faker.Faker()

    student_amount = 50
    groupe_amount = 3
    lesson_amount = 8
    teacher_amount = 5
    score_amount = 20

    with DBSession() as session:

        groupes = []

        for _ in range(groupe_amount):
            groupe = Groupe(name = fake_data.unique.company())
            groupes.append(groupe)
            session.add(groupe)

        session.commit()

        students = []

        for num in range(student_amount):
            student = Student(
                name = fake_data.unique.name(),
                groupe_id = groupes[num % groupe_amount - 1].id
            )
            students.append(student)
            session.add(student)
        
        session.commit()

        teachers = []

        for _ in range(teacher_amount):
            teacher = Teacher(name = fake_data.unique.name())
            teachers.append(teacher)
            session.add(teacher)
        
        session.commit()

        lessons = []

        for num in range(lesson_amount):
            lesson = Lesson(
                lesson = fake_data.unique.catch_phrase(),
                teacher_id = teachers[num % teacher_amount - 1].id
            )
            lessons.append(lesson)
            session.add(lesson)

        session.commit()

        for i in range(student_amount):
            for j in range(score_amount):
                score = Score(
                    score=random.uniform(1.0, 12.0),
                    date = fake_data.date_time(),
                    student_id = students[i].id,
                    lesson_id = lessons[j % lesson_amount - 1].id
                )
                session.add(score)

        session.commit()


if __name__ == "__main__":
    init_db()
