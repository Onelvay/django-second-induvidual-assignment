from celery import shared_task
from django.core.mail import send_mail

@shared_task
def notify_grade_update(student_email, course_name, grade):
    subject = f'Grade Update for {course_name}'
    message = f'Your grade has been updated to: {grade}'
    send_mail(subject, message, 'noreply@school.com', [student_email])
