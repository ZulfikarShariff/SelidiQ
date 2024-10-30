from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv  # Importing load_dotenv to load environment variables
from werkzeug.security import check_password_hash  # Import check_password_hash for password verification
import os

# Load environment variables from the .env file
load_dotenv()  # Load the .env file to get environment variables

app = Flask(__name__)

# Configuring the PostgreSQL database connection dynamically using DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://u7kh03ggcqg96d:p0bf845ecc0e5562763587f65edacb0679737a148c270fae6fb12323b4cc4e871@c9pv5s2sq0i76o.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d8c5jb85betbke').replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the secret key for the application using SECRET_KEY from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '67aac01bf8adc967fe1233d9904ea18e')

# Print statement for debugging to verify that the database URL is correctly loaded
print("Database URL:", os.getenv('DATABASE_URL'))

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Defining the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=False)
    preferred_learning_style = db.Column(db.String(50), nullable=True)
    creativity_level = db.Column(db.Integer, nullable=True)
    critical_thinking_skill = db.Column(db.Integer, nullable=True)
    subjects = db.relationship('Subject', backref='student', lazy=True)
    progress = db.relationship('StudentProgress', backref='student', lazy=True)

# Defining the Subject model
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

# Defining the Lesson model
class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)  # Title of the lesson
    subject = db.Column(db.String(100), nullable=False)  # New field for Subject
    content_type = db.Column(db.String(50), nullable=False)  # New field for Content Type
    complexity_level = db.Column(db.String(50), nullable=False)  # New field for Complexity Level
    engagement_level = db.Column(db.String(50), nullable=True)  # New field for Engagement Level
    year_level = db.Column(db.Integer, nullable=False)  # Year level (7-12)
    engagement_activity = db.Column(db.Text, nullable=False)
    learning_intention = db.Column(db.Text, nullable=False)
    success_criteria = db.Column(db.Text, nullable=False)
    vocabulary = db.Column(db.Text, nullable=True)
    explicit_teaching = db.Column(db.Text, nullable=False)
    examples = db.Column(db.Text, nullable=True)
    tasks = db.Column(db.Text, nullable=False)  # Tasks for students (research, discussions, etc.)
    reflection = db.Column(db.Text, nullable=True)

# Defining the StudentProgress model
class StudentProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    engagement_rating = db.Column(db.Integer, nullable=True)  # Rating of engagement (e.g., 1-5)
    reflection_feedback = db.Column(db.Text, nullable=True)  # Student's reflection feedback
    task_completion_status = db.Column(db.String(50), nullable=True)  # Status of tasks (e.g., Completed, In Progress)

# Route for index page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# Route for Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Query the user by username
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and if the password matches the hashed password in the database
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful.', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid password. Please try again.', 'danger')
        else:
            flash('Username does not exist. Please try again.', 'danger')

    return render_template('login.html')

# Route to create a new lesson
@app.route('/upload_lesson', methods=['GET', 'POST'])
def upload_lesson():
    if request.method == 'POST':
        data = request.form
        new_lesson = Lesson(
            title=data['title'],
            subject=data['subject'],  # New field
            content_type=data['content_type'],  # New field
            complexity_level=data['complexity_level'],  # New field
            engagement_level=data.get('engagement_level'),  # New field
            year_level=int(data['year_level']),
            engagement_activity=data['engagement_activity'],
            learning_intention=data['learning_intention'],
            success_criteria=data['success_criteria'],
            vocabulary=data.get('vocabulary'),
            explicit_teaching=data['explicit_teaching'],
            examples=data.get('examples'),
            tasks=data['tasks'],
            reflection=data.get('reflection')
        )
        db.session.add(new_lesson)
        db.session.commit()
        flash('Lesson uploaded successfully.', 'success')
        return redirect(url_for('lessons'))
    return render_template('upload_lesson.html')

# Route to view all lessons
@app.route('/lessons', methods=['GET'])
def lessons():
    lessons = Lesson.query.all()
    return render_template('lessons.html', lessons=lessons)

# Route to display the create student form
@app.route('/create_student', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        data = request.form
        # Create the student object
        new_student = Student(
            first_name=data['first_name'],
            middle_name=data.get('middle_name'),
            last_name=data['last_name'],
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
        student.first_name = data.get('first_name', student.first_name)
        student.middle_name = data.get('middle_name', student.middle_name)
        student.last_name = data.get('last_name', student.last_name)
        student.preferred_learning_style = data.get('preferred_learning_style', student.preferred_learning_style)
        student.creativity_level = int(data.get('creativity_level', student.creativity_level))
        student.critical_thinking_skill = int(data.get('critical_thinking_skill', student.critical_thinking_skill))
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

# Route to edit a lesson
@app.route('/edit_lesson/<int:lesson_id>', methods=['GET', 'POST'])
def edit_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if request.method == 'POST':
        # Update lesson details based on form input
        lesson.title = request.form['title']
        lesson.subject = request.form['subject']  # New field
        lesson.content_type = request.form['content_type']  # New field
        lesson.complexity_level = request.form['complexity_level']  # New field
        lesson.engagement_level = request.form.get('engagement_level')  # New field
        lesson.engagement_activity = request.form['engagement_activity']
        lesson.learning_intention = request.form['learning_intention']
        lesson.success_criteria = request.form['success_criteria']
        lesson.vocabulary = request.form.get('vocabulary')
        lesson.explicit_teaching = request.form['explicit_teaching']
        lesson.examples = request.form.get('examples')
        lesson.tasks = request.form['tasks']
        lesson.reflection = request.form.get('reflection')

        db.session.commit()
        flash('Lesson updated successfully', 'success')
        return redirect(url_for('lessons'))

    return render_template('edit_lesson.html', lesson=lesson)

# Route to delete a lesson
@app.route('/delete_lesson/<int:lesson_id>', methods=['POST'])
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    db.session.delete(lesson)
    db.session.commit()
    flash('Lesson deleted successfully', 'success')
    return redirect(url_for('lessons'))

# Admin Dashboard Route
@app.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    return render_template('admin_dashboard.html')

# Teacher Dashboard Route
@app.route('/teacher_dashboard', methods=['GET'])
def teacher_dashboard():
    return render_template('teacher_dashboard.html')

# Student Dashboard Route
@app.route('/student_dashboard/<int:student_id>', methods=['GET'])
def student_dashboard(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student_dashboard.html', student=student)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't already exist

    # Get the port from the environment variable for Heroku, default to 5001 if not available
    port = int(os.environ.get('FLASK_PORT', 5002))
    app.run(host='0.0.0.0', port=port)

