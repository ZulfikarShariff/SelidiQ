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
    year_level = db.Column(db.Integer, nullable=True)  # Added year_level for better scheduling compatibility
    students = db.relationship('Student', secondary=student_subject, back_populates='subjects')
    timetables = db.relationship('Timetable', backref='subject', lazy=True)  # Added relationship to Timetable

# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    year_level = db.Column(db.Integer, nullable=True)
    preferred_learning_style = db.Column(db.String(50), nullable=True)
    creativity_level = db.Column(db.Integer, nullable=True)
    critical_thinking_skill = db.Column(db.Integer, nullable=True)
    subjects = db.relationship('Subject', secondary=student_subject, back_populates='students', lazy='joined')
    progress = db.relationship('StudentProgress', backref='student', lazy=True)
    interests = db.relationship('StudentInterest', backref='student', lazy=True)
    skill_bands = db.relationship('StudentSkillBand', backref='student', lazy=True)  # Fixed the backref name for consistency
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))

# Define the StudentInterest model for personalized learning
class StudentInterest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    interest = db.Column(db.String(100), nullable=False)

# Define the Teacher model
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)  # Password might not always be mandatory
    role = db.Column(db.String(50), nullable=True)  # For roles like "Teacher", "Domain Head"
    classes = db.relationship('Class', backref='teacher', lazy=True)
    lessons = db.relationship('Lesson', back_populates='owner')
    timetables = db.relationship('Timetable', backref='teacher', lazy=True)  # Added relationship to Timetable

# Define the Class model
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)  # Consider converting to a ForeignKey if subject model changes
    year_level = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    students = db.relationship('Student', backref='class', lazy=True)
    timetables = db.relationship('Timetable', backref='class', lazy=True)  # Added relationship to Timetable

# Define the Timetable model
class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    day_of_week = db.Column(db.String(50), nullable=False)  # Consider using ENUM for day names for consistency
    period_start = db.Column(db.Integer, nullable=False)  # Period number, assuming 1, 2, 3, etc.
    period_end = db.Column(db.Integer, nullable=False)  # Typically same as period_start for single periods
    is_double_period = db.Column(db.Boolean, default=False)

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
    assigned_by = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    sequence_order = db.Column(db.Integer, nullable=True)
    prerequisite_lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=True)
    explicit_teaching_images = db.Column(db.Text, nullable=True)
    content_images = db.Column(db.Text, nullable=True)
    prerequisite_lesson = db.relationship('Lesson', remote_side=[id])  # Self-referencing for prerequisites
    owner = db.relationship('Teacher', back_populates='lessons')

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
