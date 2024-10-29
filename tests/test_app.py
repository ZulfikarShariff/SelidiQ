import pytest
from app import app, db, Student, Subject
from sqlalchemy.orm import Session

@pytest.fixture
def client():
    # Setup: Create a test client and initialize the database
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for tests

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables in the in-memory database
        yield client

    # Teardown: Drop all tables
    with app.app_context():
        db.drop_all()

# Test: Home Page Route
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Assuming 'Welcome' is on the index page

# Test: Create Student
def test_create_student(client):
    response = client.post('/create_student', data={
        'name': 'John Doe',
        'preferred_learning_style': 'visual',
        'creativity_level': 4,
        'critical_thinking_skill': 5,
        'math_score': 85,
        'art_score': 90,
        'history_score': 75
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"John Doe" in response.data  # Verify that the student's name appears on the page

# Test: View All Students
def test_view_students(client):
    with app.app_context():
        # Create a student to view
        student = Student(name='Jane Doe', preferred_learning_style='auditory', creativity_level=3, critical_thinking_skill=4)
        db.session.add(student)
        db.session.commit()

        # Use session.get() to fetch the student again
        session = db.session
        student = session.get(Student, student.id)

    response = client.get('/students')
    assert response.status_code == 200
    assert b"Jane Doe" in response.data  # Verify that the student's name appears on the students page

# Test: Update Student
def test_update_student(client):
    with app.app_context():
        # Create a student to update
        student = Student(name='Alice', preferred_learning_style='kinesthetic', creativity_level=3, critical_thinking_skill=4)
        db.session.add(student)
        db.session.commit()

        # Use session.get() to fetch the student again
        session = db.session
        student = session.get(Student, student.id)

    response = client.post(f'/update_student/{student.id}', data={
        'name': 'Alice Updated',
        'preferred_learning_style': 'visual',
        'creativity_level': 5,
        'critical_thinking_skill': 4
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Alice Updated" in response.data  # Verify that the updated name appears

# Test: Delete Student
def test_delete_student(client):
    with app.app_context():
        # Create a student to delete
        student = Student(name='Bob', preferred_learning_style='auditory', creativity_level=2, critical_thinking_skill=3)
        db.session.add(student)
        db.session.commit()

        # Use session.get() to fetch the student again
        session = db.session
        student = session.get(Student, student.id)

    response = client.post(f'/delete_student/{student.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Bob" not in response.data  # Verify that the student's name no longer appears

# Test: Add Subject to Student
def test_add_subject(client):
    with app.app_context():
        # Create a student to add a subject to
        student = Student(name='Charlie', preferred_learning_style='visual', creativity_level=4, critical_thinking_skill=3)
        db.session.add(student)
        db.session.commit()

        # Use session.get() to fetch the student again
        session = db.session
        student = session.get(Student, student.id)

    response = client.post(f'/add_subject/{student.id}', json={
        'name': 'Science',
        'score': 88
    })

    assert response.status_code == 201
    assert b"Subject added successfully" in response.data

# Test: Update Subject
def test_update_subject(client):
    with app.app_context():
        # Create a student and a subject to update
        student = Student(name='David', preferred_learning_style='kinesthetic', creativity_level=3, critical_thinking_skill=4)
        db.session.add(student)
        db.session.commit()

        # Use session.get() to fetch the student again
        session = db.session
        student = session.get(Student, student.id)

        # Create a subject for the student
        subject = Subject(name='Biology', score=70, student_id=student.id)
        db.session.add(subject)
        db.session.commit()

        # Use session.get() to fetch the subject again
        subject = session.get(Subject, subject.id)

    response = client.put(f'/update_subject/{subject.id}', json={
        'name': 'Advanced Biology',
        'score': 95
    })

    assert response.status_code == 200
    assert b"Subject updated successfully" in response.data

# Test: Delete Subject
def test_delete_subject(client):
    with app.app_context():
        # Create a student and a subject to delete
        student = Student(name='Eve', preferred_learning_style='visual', creativity_level=5, critical_thinking_skill=5)
        db.session.add(student)
        db.session.commit()

        # Use session.get() to fetch the student again
        session = db.session
        student = session.get(Student, student.id)

        # Create a subject for the student
        subject = Subject(name='Physics', score=92, student_id=student.id)
        db.session.add(subject)
        db.session.commit()

        # Use session.get() to fetch the subject again
        subject = session.get(Subject, subject.id)

    response = client.delete(f'/delete_subject/{subject.id}')
    assert response.status_code == 200
    assert b"Subject deleted successfully" in response.data

# Test: Access Student Dashboard
def test_student_dashboard(client):
    with app.app_context():
        # Create a student to view the dashboard
        student = Student(name='Frank', preferred_learning_style='auditory', creativity_level=2, critical_thinking_skill=4)
        db.session.add(student)
        db.session.commit()

        # Use session.get() to fetch the student again
        session = db.session
        student = session.get(Student, student.id)

    response = client.get(f'/student_dashboard/{student.id}')
    assert response.status_code == 200
    assert b"Frank" in response.data  # Verify the student dashboard shows the student's name

