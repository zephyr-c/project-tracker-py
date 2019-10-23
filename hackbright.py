"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    row = db_cursor.fetchone()

    print("Student: {} {}\nGitHub account: {}".format(row[0], row[1], row[2]))


def make_new_student(fname, lname, github_user):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    QUERY = """
        INSERT INTO students (first_name, last_name, github)
            VALUES (:first_name, :last_name, :github)
    """

    db.session.execute(QUERY, {'first_name': fname,
                                'last_name': lname,
                                'github': github_user})

    db.session.commit()

    print(f"Successfully added student: {fname} {lname}")

def get_project_by_title(project_title):
    """Given a project title, print information about the project."""
    QUERY = """ 
        SELECT * 
        FROM projects 
        WHERE title = :title 
        """

    db_cursor = db.session.execute(QUERY, {'title':project_title})

    result = db_cursor.fetchone()
    p_id, title, description, max_grade = result

    print(f"Project Title: {title}\nProject Description: {description}\nMaximum Grade: {max_grade}")


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    QUERY = """
    SELECT grade 
    FROM grades
    WHERE student_github = :github AND project_title = :title
    """

    db_cursor = db.session.execute(QUERY, {'github':github,
                                            'title':title})

    result = db_cursor.fetchone()

    print(f'Student grade: {result[0]}')


def assign_grade(input_github, input_grade, input_title):
    """Assign a student a grade on an assignment and print a confirmation."""
    QUERY = """
        INSERT INTO grades (student_github, project_title, grade)
            VALUES (:github, :title, :grade) 
    """

    db.session.execute(QUERY, {'github':input_github,
                                'title':input_title,
                                'grade':input_grade})
    db.session.commit()

    print(f"Successfully added grade for {input_github} on {input_title} project")

def add_project(input_project_title, input_description, input_max_grade):
    """Add a project with description and maximum grade and print confirmation."""
    QUERY = """
        INSERT INTO projects (title, description, max_grade)
            VALUES (:title, :description, :max_grade)
    """

    db.session.execute(QUERY, {'title': input_project_title,
                                'description': input_description,
                                'max_grade': input_max_grade})

    db.session.commit()

    print(f"Successfully added {input_project_title}.")


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received
    as a command.
    """

    command = None

    while command != "quit":
        input_string = input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        elif command == 'project_title':
            #> project_title Markov
            project_title = " ".join(args)
            get_project_by_title(project_title)

        elif command == 'get_grade':
            github = args[0]
            title = " ".join(args[1:])
            get_grade_by_github_title(github, title)

        elif command == 'add_grade':
            #> add_grade jhacks 89 Wits and Wagers
            github, grade = args[:2]
            title = " ".join(args[2:])
            assign_grade(github, grade, title)

        else:
            if command != "quit":
                print("Invalid Entry. Try again.")


if __name__ == "__main__":
    connect_to_db(app)

    #handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
