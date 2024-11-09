# simulate_student_interaction.py

from selidiq.models import db, Student, StudentProgress
from lesson_autogenerator import recommend_or_generate_lesson

def simulate_student_progress(student_id):
    student = Student.query.get(student_id)
    next_lesson = recommend_or_generate_lesson(student)

    if next_lesson:
        # Simulate interaction and record progress
        progress = StudentProgress(
            student_id=student.id,
            lesson_id=next_lesson.id,
            engagement_rating=random.randint(1, 5),
            task_completion_status=random.choice(['completed', 'incomplete'])
        )
        db.session.add(progress)
        db.session.commit()

# Simulate for all students
for student in Student.query.all():
    simulate_student_progress(student.id)

