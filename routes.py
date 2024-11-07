# selidiq/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from selidiq import db
from selidiq.models import Student, Subject, Teacher, Class, Lesson, StudentProgress

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

# Teacher Dashboard - Accessible without login
@main.route('/teacher_dashboard', methods=['GET'])
def teacher_dashboard():
    return render_template('teacher_dashboard.html')

# Student Dashboard - Accessible without login
@main.route('/student_dashboard', methods=['GET'])
def student_dashboard():
    student = Student.query.first()  # Example: Replace with actual logic to retrieve the logged-in student
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
        
        # Assign current user or default teacher as assigned_by and owner_id
        assigned_by = current_user.id  # Get actual logged-in user ID
        owner_id = current_user.id

        new_lesson = Lesson(
            title=title,
            year_level=year_level,
            subject=subject,
            content_type=content_type,
            learning_intention=learning_intention,
            success_criteria=success_criteria,
            explicit_teaching=explicit_teaching,
            tasks=tasks,
            content=content,
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


    return render_template('create_lesson_plan.html')

# Route to view all lessons without login
@main.route('/view_teacher_lessons', methods=['GET'])
def view_teacher_lessons():
    lessons = Lesson.query.all()  # Fetch all lessons, as there’s no login and user tracking
    return render_template('view_teacher_lessons.html', lessons=lessons)

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

