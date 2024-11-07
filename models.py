from selidiq import db
from flask_login import UserMixin

# Association table for Student and Subject
student_subject = db.Table('student_subject',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True)
)

# Define the User model for authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=True)  # Optional, for role-based permissions

# Define the Subject model
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    students = db.relationship('Student', secondary=student_subject, back_populates='subjects')

# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    year_level = db.Column(db.Integer, nullable=False)
    preferred_learning_style = db.Column(db.String(50), nullable=True)
    creativity_level = db.Column(db.Integer, nullable=True)
    critical_thinking_skill = db.Column(db.Integer, nullable=True)
    subjects = db.relationship('Subject', secondary=student_subject, back_populates='students', lazy='joined')
    progress = db.relationship('StudentProgress', backref='student', lazy=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))

# Define the Teacher model
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=True)  # For roles like "Teacher", "Domain Head"
    classes = db.relationship('Class', backref='teacher', lazy=True)
    lessons = db.relationship('Lesson', back_populates='owner')  # Teacher owns lessons

# Define the Class model
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    year_level = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    students = db.relationship('Student', backref='class', lazy=True)

# Define the StudentProgress model
class StudentProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    engagement_rating = db.Column(db.Integer, nullable=True)
    reflection_feedback = db.Column(db.Text, nullable=True)
    task_completion_status = db.Column(db.String(50), nullable=True)

# Define the Lesson model
class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)
    complexity_level = db.Column(db.String(50), nullable=True)
    engagement_level = db.Column(db.String(50), nullable=True)
    year_level = db.Column(db.Integer, nullable=False)
    engagement_activity = db.Column(db.Text, nullable=True)
    learning_intention = db.Column(db.Text, nullable=False)
    success_criteria = db.Column(db.Text, nullable=False)
    vocabulary = db.Column(db.Text, nullable=True)
    explicit_teaching = db.Column(db.Text, nullable=False)
    tasks = db.Column(db.Text, nullable=False)
    reflection = db.Column(db.Text, nullable=True)
    critical_thinking_goal = db.Column(db.String(50), nullable=True)
    creativity_goal = db.Column(db.String(50), nullable=True)
    lesson_type = db.Column(db.String(50), nullable=True, default='General')
    assigned_by = db.Column(db.String(100), nullable=False)  # Assumes teacher's name or role
    owner_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=True)  # Links to Teacher ID
    content = db.Column(db.Text, nullable=False)

    # Relationship to the owner/teacher
    owner = db.relationship('Teacher', back_populates='lessons', lazy=True)

# Define the Core Curriculum Module model
class CoreCurriculumModule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    year_level = db.Column(db.Integer, nullable=False)
    module_content = db.Column(db.Text, nullable=False)

# Define the Extended Pathway model
class ExtendedPathway(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    difficulty_level = db.Column(db.String(50), nullable=False)
    module_content = db.Column(db.Text, nullable=False)

# Define the Student Skill Band model
class StudentSkillBand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    skill_band = db.Column(db.String(50), nullable=False)

    student = db.relationship('Student', backref='skill_bands', lazy=True)

