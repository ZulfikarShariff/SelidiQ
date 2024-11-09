# lesson_autogenerator.py

from selidiq.models import Lesson, Student, db
import random

def recommend_or_generate_lesson(student):
    # Retrieve completed lessons
    completed_lesson_ids = [p.lesson_id for p in student.progress if p.task_completion_status == 'completed']

    # Determine next lesson in sequence or generate if none available
    next_lesson = Lesson.query.filter(
        ~Lesson.id.in_(completed_lesson_ids),  # Exclude completed lessons
        Lesson.prerequisite_lesson_id.in_(completed_lesson_ids),  # Prerequisites met
        Lesson.level <= student.year_level
    ).order_by(Lesson.sequence_order).first()

    # Generate new lesson if none available
    if not next_lesson:
        interest = random.choice(student.interests) if student.interests else "General"
        title = f"{interest}-Themed Math"
        new_lesson = Lesson(
            title=title,
            subject="Math",
            level=student.year_level,
            content_type="Interactive",
            content=f"Exploring math through {interest}",
            is_generated=True
        )
        db.session.add(new_lesson)
        db.session.commit()
        return new_lesson
    return next_lesson

