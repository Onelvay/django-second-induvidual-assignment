from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from students.models import Student
from courses.models import Course
from .models import Attendance

User = get_user_model()

class AttendanceAPITest(APITestCase):
    def setUp(self):
        # Создаем пользователей и данные для тестов
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', role='admin')
        self.student_user = User.objects.create_user(username='student', password='studentpass', role='student')
        self.student = Student.objects.create(user=self.student_user, dob="2000-01-01")
        self.course = Course.objects.create(name="Math", description="Basic Math", instructor=self.admin_user)
        self.attendance = Attendance.objects.create(
            student=self.student, course=self.course, date="2024-11-19", status="present"
        )

    def test_get_attendance_as_student(self):
        self.client.login(username='student', password='studentpass')
        response = self.client.get('/api/attendance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_attendance_as_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post('/api/attendance/', {
            'student': self.student.id,
            'course': self.course.id,
            'date': "2024-11-20",
            'status': "absent"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
