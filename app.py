from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user
from dotenv import load_dotenv
from werkzeug.security import check_password_hash
from sqlalchemy.orm import joinedload
import os
import logging

# Add these imports as per the provided snippet:
from selidiq import create_app, db
from flask_migrate import Migrate
from selidiq.models import Student, Subject, Teacher, Class, StudentProgress, Lesson

# Load environment variables from the .env file
load_dotenv()

# Create the Flask application instance using the factory function
app = create_app()  # Create the `app` here, before defining routes

# Setup logging (if not already setup in `create_app`)
logging.basicConfig(level=logging.INFO)


# Route for index page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
# Route to create a new student
@app.route('/create_student', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        preferred_learning_style = request.form.get('preferred_learning_style')
        creativity_level = request.form.get('creativity_level')
        critical_thinking_skill = request.form.get('critical_thinking_skill')

        # Validate the form data and add the new student to the database
        if not first_name or not last_name:
            flash('First and Last Name are required.', 'danger')
        else:
            new_student = Student(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                preferred_learning_style=preferred_learning_style,
                creativity_level=int(creativity_level) if creativity_level else None,
                critical_thinking_skill=int(critical_thinking_skill) if critical_thinking_skill else None
            )
            db.session.add(new_student)
            db.session.commit()
            flash(f'Student "{first_name} {last_name}" added successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('create_student.html')

from flask import current_app
from flask_login import login_user

# Route for Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_app.config['ENV'] == 'development':
        # Automatically log in a hard-coded user for development purposes
        with app.app_context():
            user = User.query.first()  # Automatically log in the first user for testing
        if user:
            login_user(user)
            flash('Development login successful.', 'success')
            return redirect(url_for('index'))
    
    # Actual login process for other environments
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Query the user by username
        with app.app_context():
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

        
# Route for admin_dashboard
@app.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    with app.app_context():
        students = Student.query.options(joinedload(Student.subjects)).all()
        subjects = Subject.query.all()
        classes = Class.query.all()
        teachers = Teacher.query.all()
        return render_template('admin_dashboard.html', students=students, subjects=subjects, classes=classes, teachers=teachers)

# Route to create a class
@app.route('/create_class', methods=['GET', 'POST'])
def create_class():
    if request.method == 'POST':
        name = request.form.get('name')
        subject = request.form.get('subject')
        year_level = request.form.get('year_level')
        # Add additional class-specific information as needed
        
        if not name or not subject or not year_level:
            flash('All fields are required.', 'danger')
        else:
            new_class = Class(name=name, subject=subject, year_level=year_level)
            db.session.add(new_class)
            db.session.commit()
            flash(f'Class "{name}" created successfully.', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('create_class.html')

# Route to view all classes
@app.route('/view_classes', methods=['GET'])
def view_classes():
    with app.app_context():
        classes = Class.query.options(joinedload(Class.students)).all()  # Eager load students for each class
        return render_template('view_classes.html', classes=classes)
        
# Route to display and update a student's details
@app.route('/update_student/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    with app.app_context():
        # Fetch the student with eager loading for related subjects
        student = db.session.query(Student).options(joinedload(Student.subjects)).get_or_404(id)

        if request.method == 'POST':
            data = request.form
            # Update the student's basic information
            student.first_name = data.get('first_name', student.first_name)
            student.middle_name = data.get('middle_name', student.middle_name)
            student.last_name = data.get('last_name', student.last_name)
            student.preferred_learning_style = data.get('preferred_learning_style', student.preferred_learning_style)
            student.creativity_level = int(data.get('creativity_level', student.creativity_level))
            student.critical_thinking_skill = int(data.get('critical_thinking_skill', student.critical_thinking_skill))

            # Update subjects and their scores if provided
            for subject in student.subjects:
                subject_score = data.get(f'subject_score_{subject.id}')
                if subject_score:
                    subject.score = float(subject_score)

            # Commit the updated student data to the database
            db.session.commit()
            return redirect(url_for('view_students'))

        # Render the update_student template with the student's data
        return render_template('update_student.html', student=student)

# Route to create a new subject
@app.route('/create_subject', methods=['GET', 'POST'])
def create_subject():
    if request.method == 'POST':
        subject_name = request.form['subject_name']
        if not subject_name:
            flash('Subject name is required.', 'danger')
        else:
            existing_subject = Subject.query.filter_by(name=subject_name).first()
            if existing_subject:
                flash('Subject already exists.', 'info')
            else:
                new_subject = Subject(name=subject_name)
                db.session.add(new_subject)
                db.session.commit()
                flash(f'Subject "{subject_name}" created successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('create_subject.html')

# Route to assign a subject to a student
@app.route('/assign_subject/<int:student_id>', methods=['POST'])
def assign_subject(student_id):
    student = Student.query.get_or_404(student_id)
    subject_id = request.form.get('subject_id')

    # Check if the subject exists
    subject = Subject.query.get_or_404(subject_id)

    # Assign subject to student only if it's not already assigned
    if subject not in student.subjects:
        student.subjects.append(subject)
        db.session.commit()
        flash(f'Successfully assigned {subject.name} to {student.first_name} {student.last_name}.', 'success')
    else:
        flash(f'Subject {subject.name} is already assigned to {student.first_name} {student.last_name}.', 'info')

    return redirect(url_for('admin_dashboard'))

# Route to assign a subject to a class of students
@app.route('/assign_subject_to_class', methods=['POST'])
def assign_subject_to_class():
    subject_id = request.form.get('subject_id')
    student_ids = request.form.getlist('student_ids')  # Get list of student IDs

    if not subject_id or not student_ids:
        return jsonify({'error': 'Subject and list of student IDs are required'}), 400

    # Check if the subject exists
    subject = Subject.query.get_or_404(subject_id)

    # Assign subject to each student if it's not already assigned
    for student_id in student_ids:
        student = Student.query.get_or_404(student_id)
        if subject not in student.subjects:
            student.subjects.append(subject)

    db.session.commit()
    flash(f'Successfully assigned {subject.name} to the selected students.', 'success')
    return redirect(url_for('admin_dashboard'))

# Route to view an individual student without requiring login
@app.route('/view_student/<int:student_id>', methods=['GET'])
def view_student(student_id):
    with app.app_context():
        student = Student.query.options(joinedload(Student.subjects)).get_or_404(student_id)

        # Mock logic to determine user role (admin or teacher)
        # For example, this is hardcoded for testing purposes. You can update it based on your requirements.
        user_role = request.args.get('role', 'admin')  # Default to 'admin' if no role is provided

        # Allow admins to view student
        if user_role == 'admin':
            return render_template('view_student.html', student=student)

        # Allow teachers to view students they teach
        elif user_role == 'teacher':
            # Mock logic: Allow the teacher to view student (assuming teacher is linked to the student)
            # For now, we'll just allow all teachers to view any student for simplicity
            return render_template('view_student.html', student=student)

        # If the role is neither admin nor teacher, deny access
        flash('You do not have permission to view this student.', 'danger')
        return redirect(url_for('teacher_dashboard'))

# Route to view all students
@app.route('/view_students', methods=['GET'])
def view_students():
    search_query = request.args.get('search_query', '')
    with app.app_context():
        # If there is a search query, filter students by first or last name
        if search_query:
            students = Student.query.filter(
                (Student.first_name.ilike(f"%{search_query}%")) |
                (Student.last_name.ilike(f"%{search_query}%"))
            ).options(joinedload(Student.subjects)).all()
        else:
            students = Student.query.options(joinedload(Student.subjects)).all()
        return render_template('view_students.html', students=students)

# Route to update a subject score
@app.route('/update_assigned_subject_score/<int:student_id>/<int:subject_id>', methods=['PUT'])
def update_assigned_subject_score(student_id, subject_id):
    subject_entry = db.session.query(student_subject).filter_by(student_id=student_id, subject_id=subject_id).first()
    data = request.get_json()

    if subject_entry:
        subject_entry.score = data.get('score', subject_entry.score)
        db.session.commit()

    return jsonify({'message': 'Assigned subject score updated successfully'}), 200

# Route to delete a subject score
@app.route('/delete_assigned_subject/<int:student_id>/<int:subject_id>', methods=['DELETE'])
def delete_assigned_subject(student_id, subject_id):
    subject_entry = db.session.query(student_subject).filter_by(student_id=student_id, subject_id=subject_id).first()
    if subject_entry:
        db.session.delete(subject_entry)
        db.session.commit()
    return jsonify({'message': 'Assigned subject deleted successfully'}), 200

# Route to create a Core Curriculum Module
@app.route('/create_core_module', methods=['GET', 'POST'])
def create_core_module():
    if request.method == 'POST':
        data = request.form
        new_module = CoreCurriculumModule(
            title=data['title'],
            subject=data['subject'],
            year_level=int(data['year_level']),
            module_content=data['module_content']
        )
        db.session.add(new_module)
        db.session.commit()
        flash('Core Curriculum Module created successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('create_core_module.html')

# Route to create an Extended Pathway
@app.route('/create_extended_pathway', methods=['GET', 'POST'])
def create_extended_pathway():
    if request.method == 'POST':
        data = request.form
        new_pathway = ExtendedPathway(
            title=data['title'],
            subject=data['subject'],
            difficulty_level=data['difficulty_level'],
            module_content=data['module_content']
        )
        db.session.add(new_pathway)
        db.session.commit()
        flash('Extended Pathway created successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('create_extended_pathway.html')

# Route to assign a skill band to a student
@app.route('/assign_skill_band/<int:student_id>', methods=['GET', 'POST'])
def assign_skill_band(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        data = request.form
        new_skill_band = StudentSkillBand(
            student_id=student.id,
            subject=data['subject'],
            skill_band=data['skill_band']
        )
        db.session.add(new_skill_band)
        db.session.commit()
        flash('Skill band assigned successfully.', 'success')
        return redirect(url_for('view_students'))
    return render_template('assign_skill_band.html', student=student)

# Route to upload lessons for Domain Head
# Route to upload lessons for Domain Head
@app.route('/add_domain_lesson', methods=['GET', 'POST'])
def add_domain_lesson():
    if current_user.role != 'Domain Head':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        title = request.form.get('title')
        subject = request.form.get('subject')
        complexity_level = request.form.get('complexity_level')
        year_level = request.form.get('year_level')
        lesson_type = request.form.get('lesson_type', 'Domain')  # Assign a default value

        # Add additional fields as needed

        if not title or not subject or not complexity_level or not year_level:
            flash('All fields are required.', 'danger')
        else:
            new_lesson = Lesson(
                title=title,
                subject=subject,
                complexity_level=complexity_level,
                year_level=year_level,
                lesson_type=lesson_type,  # Ensure there is a comma here
                assigned_by=f"{current_user.first_name} {current_user.last_name}",
                owner_id=current_user.id
            )
            db.session.add(new_lesson)
            db.session.commit()
            flash(f'Lesson "{title}" added successfully to the domain.', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_domain_lesson.html')

# Route for teacher_dashboard
@app.route('/teacher_dashboard', methods=['GET'])
def teacher_dashboard():
    with app.app_context():
        students = Student.query.options(joinedload(Student.subjects)).all()
        lessons = Lesson.query.all()
        return render_template('teacher_dashboard.html', students=students, lessons=lessons)

# Route for the teacher to view their classes
@app.route('/view_my_classes', methods=['GET'])
def view_my_classes():
    teacher_id = request.args.get('teacher_id', 1)  # Using a hard-coded teacher ID for now
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        print(f"Teacher with ID {teacher_id} not found.")
        return "Teacher not found", 404
    else:
        print(f"Found Teacher: {teacher.first_name} {teacher.last_name}")

    classes = teacher.classes
    print(f"Classes for Teacher ID {teacher_id}: {[c.name for c in classes]}")

    return render_template('view_my_classes.html', classes=classes)

# Route to view student's progress
@app.route('/student_progress', methods=['GET'])
def student_progress():
    # Get all students' progress for monitoring purposes
    student_progress_list = StudentProgress.query.all()
    return render_template('student_progress.html', student_progress=student_progress_list)

#Route to view teacher created lesson
@app.route('/view_teacher_lessons', methods=['GET'])
def view_teacher_lessons():
    # Mock the current user role for bypassing the login
    mock_user = {
        "role": "Teacher",
        "id": 1  # Assuming the ID of the teacher you want to use
    }

    # Bypass authentication check
    if mock_user['role'] != 'Teacher':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('teacher_dashboard'))

    # Filter lessons by the mock user's ID
    lessons = Lesson.query.filter_by(lesson_type='Teacher', owner_id=mock_user['id']).all()
    return render_template('view_teacher_lessons.html', lessons=lessons)

#Route to Update lessons
@app.route('/update_lesson/<int:id>', methods=['GET', 'POST'])
def update_lesson(id):
    lesson = Lesson.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        lesson.title = data.get('title', lesson.title)
        lesson.subject = data.get('subject', lesson.subject)
        lesson.year_level = data.get('year_level', lesson.year_level)
        lesson.content_type = data.get('content_type', lesson.content_type)
        lesson.lesson_type = data.get('lesson_type', lesson.lesson_type) or "General"

        # Commit changes to the database
        db.session.commit()
        flash(f'Lesson "{lesson.title}" updated successfully.', 'success')
        return redirect(url_for('teacher_dashboard'))

    return render_template('update_lesson.html', lesson=lesson)


#Route to view Domain lessons
@app.route('/view_domain_lessons', methods=['GET'])
def view_domain_lessons():
    if current_user.role not in ['Domain Head', 'Teacher']:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('teacher_dashboard'))

    # Teachers should be able to see domain lessons related to their subjects.
    if current_user.role == 'Teacher':
        lessons = Lesson.query.filter_by(lesson_type='Domain').all()
    elif current_user.role == 'Domain Head':
        lessons = Lesson.query.filter_by(lesson_type='Domain', owner_id=current_user.id).all()

    return render_template('view_domain_lessons.html', lessons=lessons)


# Route to manually create a lesson plan
@app.route('/create_lesson_plan', methods=['GET', 'POST'])
def create_lesson_plan():
    if request.method == 'POST':
        # Collect form data
        title = request.form.get('title')
        year_level = request.form.get('year_level')
        subject = request.form.get('subject')
        content = request.form.get('content')

        # Additional fields for creativity, critical thinking, etc.
        critical_thinking_goal = request.form.get('critical_thinking_goal')
        creativity_goal = request.form.get('creativity_goal')
        complexity_level = request.form.get('complexity_level')
        engagement_level = request.form.get('engagement_level')

        # Validate and save new lesson
        if title and year_level and subject and content:
            new_lesson = Lesson(
                title=title,
                year_level=year_level,
                subject=subject,
                content=content,
                critical_thinking_goal=critical_thinking_goal,
                creativity_goal=creativity_goal,
                complexity_level=complexity_level,
                engagement_level=engagement_level
            )
            db.session.add(new_lesson)
            db.session.commit()
            flash(f'Lesson Plan "{title}" created successfully.', 'success')
            return redirect(url_for('teacher_dashboard'))

        flash('All fields are required.', 'danger')
    return render_template('create_lesson_plan.html')

# Route to use AI generated plan
@app.route('/ai_lesson_generator', methods=['GET'])
def ai_lesson_generator():
    # Logic for AI Lesson Generator goes here, for now, it's a placeholder page
    return render_template('ai_lesson_generator.html')

# Route to view lesson plans
@app.route('/view_lesson_plans', methods=['GET'])
def view_lesson_plans():
    lesson_plans = Lesson.query.all()
    return render_template('view_lesson_plans.html', lesson_plans=lesson_plans)

# Route to manually group students
@app.route('/group_students', methods=['GET', 'POST'])
def group_students():
    if request.method == 'POST':
        # Placeholder logic for grouping students based on input
        student_ids = request.form.getlist('student_ids')
        group_name = request.form.get('group_name')

        if student_ids and group_name:
            # Example of saving the group information
            flash(f'Students grouped successfully under "{group_name}".', 'success')
        else:
            flash('Please select students and provide a group name.', 'danger')

        return redirect(url_for('teacher_dashboard'))

    students_list = Student.query.all()
    return render_template('group_students.html', students=students_list)

# Route for AI suggested grouping
@app.route('/ai_grouping_suggestions', methods=['GET'])
def ai_grouping_suggestions():
    # Logic to generate AI-based grouping suggestions
    suggested_groups = []  # Replace with actual AI-based logic to generate groups
    return render_template('ai_grouping_suggestions.html', suggested_groups=suggested_groups)

# Route to view class reports
@app.route('/view_reports', methods=['GET'])
def view_reports():
    with app.app_context():
        # Fetch all classes, subjects, and their associated student progress to generate reports
        classes = Class.query.all()
        subjects = Subject.query.all()
        student_progress = StudentProgress.query.all()

        return render_template('view_reports.html', classes=classes, subjects=subjects, student_progress=student_progress)


# Route to create assessment
@app.route('/create_assessment', methods=['GET', 'POST'])
def create_assessment():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        class_id = request.form.get('class_id')

        if not title or not class_id:
            flash('Title and Class are required fields.', 'danger')
        else:
            # Example: Save the assessment
            new_assessment = Assessment(
                title=title,
                description=description,
                class_id=class_id
            )
            db.session.add(new_assessment)
            db.session.commit()
            flash(f'Assessment "{title}" created successfully.', 'success')

        return redirect(url_for('teacher_dashboard'))

    classes = Class.query.all()  # Fetch all classes for selecting in the form
    return render_template('create_assessment.html', classes=classes)

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't already exist
        db.create_all()
    # Run the app
    app.run(debug=True, port=5002)

