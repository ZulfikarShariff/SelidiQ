# selidiq/routes.py

import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from selidiq import db
from selidiq.models import Student, Subject, Teacher, Class, Lesson, StudentProgress, Timetable
import random  # Placeholder for AI scheduling logic, can replace with real algorithm later

# Define allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'heic'}

# Helper function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

main = Blueprint('main', __name__)

# Route for the index page
@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

# Admin Dashboard - Accessible without login
@main.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    students = Student.query.all()
    subjects = Subject.query.all()
    classes = Class.query.all()
    teachers = Teacher.query.all()
    return render_template('admin_dashboard.html', students=students, subjects=subjects, classes=classes, teachers=teachers)

# Create Teacher - Accessible without login
@main.route('/create_teacher', methods=['GET', 'POST'])
def create_teacher():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        
        if not first_name or not last_name or not email:
            flash('First, Last Name, and Email are required.', 'danger')
        else:
            new_teacher = Teacher(first_name=first_name, last_name=last_name, email=email)
            db.session.add(new_teacher)
            db.session.commit()
            flash(f'Teacher "{first_name} {last_name}" added successfully.', 'success')
            return redirect(url_for('main.admin_dashboard'))
    return render_template('create_teacher.html')

# View All Teachers - Accessible without login
@main.route('/view_teachers', methods=['GET'])
def view_teachers():
    teachers = Teacher.query.all()
    return render_template('view_teachers.html', teachers=teachers)

# Generate Teacher Timetable Form - Accessible without login
@main.route('/generate_timetable', methods=['GET'])
def generate_timetable():
    # Render the timetable preferences form
    return render_template('timetable_preferences.html')

# View Timetable Preferences - Accessible without login
@main.route('/timetable_preferences', methods=['GET'])
def timetable_preferences():
    # Render the HTML form for collecting timetable preferences
    return render_template('timetable_preferences.html')

# Route to handle timetable generation logic
@main.route('/process_timetable_generation', methods=['POST'])
def process_timetable_generation():
    # Step 1: Extract form data
    teacher_name = request.form.get('teacher_name')
    is_full_time = request.form.get('is_full_time')
    regular_days_off = request.form.get('regular_days_off')
    max_periods_per_week = request.form.get('max_periods_per_week')
    preferred_double_periods = request.form.get('preferred_double_periods')
    class_name = request.form.get('class_name')
    year_level = request.form.get('year_level')
    periods_per_week = request.form.get('periods_per_week')
    single_double_preference = request.form.get('single_double_preference')
    subject_name = request.form.get('subject_name')
    subject_year_level = request.form.get('subject_year_level')
    periods_per_day = request.form.get('periods_per_day')
    days_per_week = request.form.get('days_per_week')
    classroom_availability = request.form.get('classroom_availability')

    # Step 2: Validate form data
    if not teacher_name or not class_name or not subject_name:
        flash('Please fill in all required fields.', 'danger')
        return redirect(url_for('main.timetable_preferences'))

    # Step 3: Store data in the database if needed
    new_teacher = Teacher(
        name=teacher_name,
        is_full_time=(is_full_time == 'yes'),
        max_periods_per_week=max_periods_per_week,
        regular_days_off=regular_days_off,
        preferred_double_periods=(preferred_double_periods == 'yes')
    )
    db.session.add(new_teacher)
    db.session.commit()

    # Similarly, add classes and subjects
    new_class = Class(name=class_name, year_level=year_level, periods_per_week=periods_per_week)
    db.session.add(new_class)
    db.session.commit()

    new_subject = Subject(name=subject_name, year_level=subject_year_level)
    db.session.add(new_subject)
    db.session.commit()

    # Step 4: Generate Timetable (Implement Logic for AI or Rule-Based Scheduling)
    timetable_entries = []
    for day in range(int(days_per_week)):
        for period in range(int(periods_per_day)):
            timetable_entries.append({
                'day': day + 1,
                'period': period + 1,
                'teacher': teacher_name,
                'class': class_name,
                'subject': subject_name
            })

    # Step 5: Save generated timetable to the database
    for entry in timetable_entries:
        new_timetable = Timetable(
            class_id=new_class.class_id,
            teacher_id=new_teacher.teacher_id,
            subject_id=new_subject.subject_id,
            day_of_week=f"Day {entry['day']}",
            period_start=entry['period'],
            period_end=entry['period'],
            is_double_period=False
        )
        db.session.add(new_timetable)
    db.session.commit()

    flash('Timetable generated successfully!', 'success')
    return redirect(url_for('main.view_timetable'))

# Route to view the generated timetable
@main.route('/view_timetable', methods=['GET'])
def view_timetable():
    # Query timetable along with related class, teacher, and subject data
    timetables = db.session.query(
        Timetable,
        Class.name.label('class_name'),
        Teacher.name.label('teacher_name'),
        Subject.name.label('subject_name')
    ).join(Class, Timetable.class_id == Class.class_id) \
     .join(Teacher, Timetable.teacher_id == Teacher.teacher_id) \
     .join(Subject, Timetable.subject_id == Subject.subject_id) \
     .all()

    return render_template('view_timetable.html', timetables=timetables)

# Manage CRT Allocation - Accessible without login
@main.route('/crt_allocation', methods=['GET'])
def crt_allocation():
    # Placeholder logic for managing CRT
    # Add your actual CRT management logic here, e.g., fetching CRT details, availability, etc.
    flash("CRT allocation feature is not yet implemented.", 'info')
    return redirect(url_for('main.admin_dashboard'))

# Predict CRT Needs - Accessible without login
@main.route('/crt_predictions', methods=['GET'])
def crt_predictions():
    # Placeholder logic for predicting CRT needs (e.g., using AI/ML models)
    flash("CRT predictions feature is not yet implemented.", 'info')
    return redirect(url_for('main.admin_dashboard'))

# Track VCE/HSC Student Outcomes - Accessible without login
@main.route('/vce_hsc_tracking', methods=['GET'])
def vce_hsc_tracking():
    # Placeholder logic to track VCE/HSC student outcomes
    # This is where you will add the logic for viewing student performance data
    flash("VCE/HSC tracking feature is not yet implemented.", 'info')
    return redirect(url_for('main.admin_dashboard'))

# AI Recommendations for Learning Pathways - Accessible without login
@main.route('/ai_recommendations', methods=['GET'])
def ai_recommendations():
    # Placeholder logic to provide AI-based learning recommendations
    # Replace this with your AI logic
    flash("AI recommendations feature is not yet implemented.", 'info')
    return redirect(url_for('main.admin_dashboard'))

# Teacher Dashboard - Accessible without login
@main.route('/teacher_dashboard', methods=['GET'])
def teacher_dashboard():
    return render_template('teacher_dashboard.html')

# Student Dashboard - Accessible without login
@main.route('/student_dashboard', methods=['GET'])
def student_dashboard():
    student = Student.query.first()  # Replace with actual logic to retrieve the logged-in student
    upcoming_lessons = Lesson.query.limit(5).all()
    return render_template('student_dashboard.html', student=student, upcoming_lessons=upcoming_lessons)

# View Students - Accessible without login
@main.route('/view_students', methods=['GET'])
def view_students():
    search_query = request.args.get('search_query', '')
    students = (Student.query.filter(
        (Student.first_name.ilike(f"%{search_query}%")) |
        (Student.last_name.ilike(f"%{search_query}%"))
    ).all() if search_query else Student.query.all())
    return render_template('view_students.html', students=students)

# View a specific student - Accessible without login
@main.route('/view_student/<int:student_id>', methods=['GET'])
def view_student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('view_student.html', student=student)

# Create Student - Accessible without login
@main.route('/create_student', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        preferred_learning_style = request.form.get('preferred_learning_style')

        if not first_name or not last_name:
            flash('First and Last Name are required.', 'danger')
        else:
            new_student = Student(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                preferred_learning_style=preferred_learning_style,
            )
            db.session.add(new_student)
            db.session.commit()
            flash(f'Student "{first_name} {last_name}" added successfully.', 'success')
            return redirect(url_for('main.admin_dashboard'))
    return render_template('create_student.html')

# The rest of the routes remain unchanged...


# Create Class - Accessible without login
@main.route('/create_class', methods=['GET', 'POST'])
def create_class():
    if request.method == 'POST':
        name = request.form.get('name')
        subject = request.form.get('subject')
        year_level = request.form.get('year_level')

        if not name or not subject or not year_level:
            flash('All fields are required.', 'danger')
        else:
            new_class = Class(name=name, subject=subject, year_level=year_level)
            db.session.add(new_class)
            db.session.commit()
            flash(f'Class "{name}" created successfully.', 'success')
            return redirect(url_for('main.admin_dashboard'))
    return render_template('create_class.html')

# View Classes - Accessible without login
@main.route('/view_classes', methods=['GET'])
def view_classes():
    classes = Class.query.all()
    return render_template('view_classes.html', classes=classes)

# Update Student - Accessible without login
@main.route('/update_student/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.first_name = request.form.get('first_name', student.first_name)
        student.middle_name = request.form.get('middle_name', student.middle_name)
        student.last_name = request.form.get('last_name', student.last_name)
        student.preferred_learning_style = request.form.get('preferred_learning_style', student.preferred_learning_style)
        db.session.commit()
        flash(f'Student "{student.first_name} {student.last_name}" updated successfully.', 'success')
        return redirect(url_for('main.view_students'))
    return render_template('update_student.html', student=student)

# Create Lesson Plan - Accessible without login
@main.route('/create_lesson_plan', methods=['GET', 'POST'])
def create_lesson_plan():
    all_lessons = Lesson.query.all()  # Fetch all lessons for the prerequisite dropdown
    if request.method == 'POST':
        title = request.form.get('title')
        year_level = request.form.get('year_level')
        subject = request.form.get('subject')
        content_type = request.form.get('content_type')
        learning_intention = request.form.get('learning_intention')
        success_criteria = request.form.get('success_criteria')
        explicit_teaching = request.form.get('explicit_teaching')
        tasks = request.form.get('tasks')
        content = request.form.get('content')
        
        # Optional fields
        vocabulary = request.form.get('vocabulary')
        engagement_activity = request.form.get('engagement_activity')
        reflection = request.form.get('reflection')
        
        # Numerical options
        complexity_level = request.form.get('complexity_level')
        engagement_level = request.form.get('engagement_level')
        critical_thinking_goal = request.form.get('critical_thinking_goal')
        creativity_goal = request.form.get('creativity_goal')
        
        # Handle file uploads for explicit teaching and content images
        explicit_teaching_image = request.files.get('explicit_teaching_image')
        content_image = request.files.get('content_image')

        # Process and save images if they are uploaded and allowed
        explicit_teaching_image_url = None
        if explicit_teaching_image and allowed_file(explicit_teaching_image.filename):
            filename = secure_filename(explicit_teaching_image.filename)
            explicit_teaching_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            explicit_teaching_image_url = url_for('static', filename=f'uploads/{filename}')

        content_image_url = None
        if content_image and allowed_file(content_image.filename):
            filename = secure_filename(content_image.filename)
            content_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            content_image_url = url_for('static', filename=f'uploads/{filename}')

        # Assign current user or default teacher as assigned_by and owner_id
        assigned_by = 1
        owner_id = 1

        new_lesson = Lesson(
            title=title,
            year_level=year_level,
            subject=subject,
            content_type=content_type,
            learning_intention=learning_intention,
            success_criteria=success_criteria,
            explicit_teaching=explicit_teaching,
            explicit_teaching_image=explicit_teaching_image_url,  # Add image URL to the lesson object
            tasks=tasks,
            content=content,
            content_image=content_image_url,  # Add content image URL
            vocabulary=vocabulary,
            engagement_activity=engagement_activity,
            reflection=reflection,
            complexity_level=complexity_level,
            engagement_level=engagement_level,
            critical_thinking_goal=critical_thinking_goal,
            creativity_goal=creativity_goal,
            assigned_by=assigned_by,
            owner_id=owner_id
        )
        
        db.session.add(new_lesson)
        db.session.commit()
        
        flash('Lesson Plan created successfully!', 'success')
        return redirect(url_for('main.view_teacher_lessons'))  # Redirect to view_teacher_lessons

    return render_template('create_lesson_plan.html', all_lessons=all_lessons)

# Route to view all lessons without login
@main.route('/view_teacher_lessons', methods=['GET'])
def view_teacher_lessons():
    sort_by = request.args.get('sort_by', 'year_level')
    sort_options = {
        'year_level': Lesson.year_level,
        'subject': Lesson.subject,
        'complexity_level': Lesson.complexity_level,
        'interest': None  # Custom handling for interest sorting
    }
    
    # Fetch student details if needed for interest alignment
    student_id = request.args.get('student_id')  # Replace with actual user logic if available
    student = Student.query.get(student_id) if student_id else None

    # Base query
    query = Lesson.query

    if student and student.interests and sort_by == 'interest':
        # Show lessons that match student interests first, then others
        lessons = sorted(
            query.all(),
            key=lambda lesson: (lesson.subject not in student.interests, lesson.year_level)
        )
    else:
        # Apply standard sorting
        sort_column = sort_options.get(sort_by, Lesson.year_level)
        lessons = query.order_by(sort_column).all()

    return render_template('view_teacher_lessons.html', lessons=lessons, sort_by=sort_by, student=student)

# View a specific lesson
@main.route('/view_lesson/<int:lesson_id>', methods=['GET'])
def view_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template('view_lesson.html', lesson=lesson)

# Edit a lesson
@main.route('/edit_lesson/<int:lesson_id>', methods=['GET', 'POST'])
def edit_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    if request.method == 'POST':
        lesson.title = request.form.get('title', lesson.title)
        lesson.subject = request.form.get('subject', lesson.subject)
        lesson.year_level = request.form.get('year_level', lesson.year_level)
        db.session.commit()
        flash('Lesson updated successfully.', 'success')
        return redirect(url_for('main.view_teacher_lessons'))
    return render_template('edit_lesson.html', lesson=lesson)

# Delete a lesson
@main.route('/delete_lesson/<int:lesson_id>', methods=['POST'])
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    db.session.delete(lesson)
    db.session.commit()
    flash('Lesson deleted successfully.', 'success')
    return redirect(url_for('main.view_teacher_lessons'))

# Assign Subject to Student - Accessible without login
@main.route('/assign_subject/<int:student_id>', methods=['POST'])
def assign_subject(student_id):
    subject_id = request.form.get('subject_id')
    if not subject_id:
        flash("Subject selection is required.", 'danger')
        return redirect(url_for('main.admin_dashboard'))

    student = Student.query.get_or_404(student_id)
    subject = Subject.query.get_or_404(subject_id)

    if subject not in student.subjects:
        student.subjects.append(subject)
        db.session.commit()
        flash(f'Successfully assigned {subject.name} to {student.first_name} {student.last_name}.', 'success')
    else:
        flash(f'Subject {subject.name} is already assigned to {student.first_name} {student.last_name}.', 'info')
    return redirect(url_for('main.admin_dashboard'))

# Delete Student - Accessible without login
@main.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash(f'Student "{student.first_name} {student.last_name}" deleted successfully.', 'success')
    return redirect(url_for('main.view_students'))

