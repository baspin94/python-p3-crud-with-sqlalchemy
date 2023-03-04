#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    # Note - why are we importing these here? Not explained. Not used during this codealong.
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    # Newly added feature
    Index('index_name', 'name')

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    # Additional attributes added
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default = datetime.now())

    # Modifying default method
    def __repr__(self):
        return f"Student {self.id}: " \
        + f"{self.name}, " \
        + f"Grade {self.grade}"


if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    # use our engine to configure a 'Session' class
    Session = sessionmaker(bind=engine)
    # use 'Session' class to create 'session' object
    session = Session()

    # Creating Records
    albert_einstein = Student(
        name = "Albert Einstein",
        email = "albert.einstein@zurich.edu",
        grade = 6,
        birthday = datetime(
            year = 1879,
            month = 3,
            day = 14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()
    print(f"New student ID is {albert_einstein.id}.")
    print(f"New student ID is {alan_turing.id}.")

    # Reading Records
    # Basic Query
    students = session.query(Student).all()
    print(students)

    # Selecting Only Certain Columns
    names = session.query(Student.name).all()
    print(names)

    # Ordering/Sorting by a Particular Column
    students_by_name = session.query(
        Student.name).order_by(
        Student.name).all()
    
    print(students_by_name)

    # Sorting in Descending Order
    students_by_grade_desc = session.query(
        Student.name, Student.grade).order_by(
        desc(Student.grade)).all()

    print(students_by_grade_desc)

    # Limiting
    # With limit()
    # oldest_student = session.query(
    #     Student.name, Student.birthday).order_by(
    #     desc(Student.grade)).limit(1).all()

    # With first()
    oldest_student = session.query(
        Student.name, Student.birthday).order_by(
        desc(Student.grade)).first()

    print(oldest_student)

    # func
    student_count = session.query(func.count(Student.id)).first()
    print(student_count)

    student_sum = session.query(func.sum(Student.id)).first()
    print(student_sum)

    # Filtering
    query = session.query(Student).filter(Student.name.like("%Alan%")).all()
    for record in query:
        print(record.name)

    # Updating Data
    # By modifying objects directly
    # for student in session.query(Student):
    #     student.grade += 1

    # session.commit()

    # print([{student.name, student.grade} for student in session.query(Student)])

    # Using the update() method
    session.query(Student).update({
        Student.grade: Student.grade + 1
    })
    print([(
        student.name,
        student.grade
    ) for student in session.query(Student)])

    # Deleting Data
    # Deleting Object In Memory
    # query = session.query(
    #     Student).filter(
    #         Student.name == "Albert Einstein"
    #     )
    # albert_einstein = query.first()
    # print(albert_einstein)

    # session.delete(albert_einstein)

    # albert_einstein = query.first()
    # print(albert_einstein)

    # Deleting Object Within Query
    query = session.query(
        Student).filter(
        Student.name == "Albert Einstein")

    query.delete()

    albert_einstein = query.first()

    print(albert_einstein)

