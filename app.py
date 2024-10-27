from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

import os

# Configuring the PostgreSQL database connection dynamically using DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', '').replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

# Defining the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    preferred_learning_style = db.Column(db.String(50), nullable=True)
    creativity_level = db.Column(db.Integer, nullable=True)
    critical_thinking_skill = db.Column(db.Integer, nullable=True)
    subjects = db.relationship('Subject', backref='student', lazy=True)

# Defining the Subject model
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# Route to display the create student form
@app.route('/create_student', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        data = request.form
        # Create the student object
        new_student = Student(
            name=data['name'],
            preferred_learning_style=data.get('preferred_learning_style'),
            creativity_level=int(data.get('creativity_level', 0)),
            critical_thinking_skill=int(data.get('critical_thinking_skill', 0))
        )
        
        # Add the student to the session
        db.session.add(new_student)
        db.session.commit()  # Commit to get student ID for subjects

        # Add subjects if provided
        subjects = [
            {'name': 'Math', 'score': data.get('math_score')},
            {'name': 'Art', 'score': data.get('art_score')},
            {'name': 'History', 'score': data.get('history_score')}
        ]

        for subject_data in subjects:
            if subject_data['score']:
                new_subject = Subject(
                    name=subject_data['name'],
                    score=float(subject_data['score']),
                    student_id=new_student.id
                )
                db.session.add(new_subject)

        # Commit the subjects to the database
        db.session.commit()

        return redirect(url_for('view_students'))
    
    return render_template('create_student.html')

# Route to display all student profiles
@app.route('/students', methods=['GET'])
def view_students():
    students = Student.query.all()
    return render_template('view_students.html', students=students)

# Route to display and update a student profile
@app.route('/update_student/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        student.name = data.get('name', student.name)
        student.preferred_learning_style = data.get('preferred_learning_style', student.preferred_learning_style)
        student.creativity_level = data.get('creativity_level', student.creativity_level)
        student.critical_thinking_skill = data.get('critical_thinking_skill', student.critical_thinking_skill)
        db.session.commit()
        return redirect(url_for('view_students'))
    
    return render_template('update_student.html', student=student)

# Route to delete a student profile
@app.route('/delete_student/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('view_students'))

# Route to add a subject to a student profile
@app.route('/add_subject/<int:student_id>', methods=['POST'])
def add_subject(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.get_json()

    if 'name' not in data or 'score' not in data:
        return jsonify({'error': 'Subject name and score are required'}), 400

    new_subject = Subject(
        name=data['name'],
        score=data['score'],
        student=student
    )
    db.session.add(new_subject)
    db.session.commit()

    return jsonify({'message': 'Subject added successfully'}), 201

# Route to update a subject
@app.route('/update_subject/<int:id>', methods=['PUT'])
def update_subject(id):
    subject = Subject.query.get_or_404(id)
    data = request.get_json()

    # Update fields
    subject.name = data.get('name', subject.name)
    subject.score = data.get('score', subject.score)

    db.session.commit()
    return jsonify({'message': 'Subject updated successfully'}), 200

# Route to delete a subject
@app.route('/delete_subject/<int:id>', methods=['DELETE'])
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    return jsonify({'message': 'Subject deleted successfully'}), 200

# Admin Dashboard Route
@app.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    return render_template('admin_dashboard.html')

# Teacher Dashboard Route
@app.route('/teacher_dashboard', methods=['GET'])
def teacher_dashboard():
    return render_template('teacher_dashboard.html')

#Student Dashboard Route
@app.route('/student_dashboard/<int:student_id>', methods=['GET'])
def student_dashboard(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student_dashboard.html', student=student)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't already exist

    # Get the port from the environment variable for Heroku, default to 5001 if not available
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)


