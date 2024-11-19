
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from students.models import Student
from courses.models import Course
from .models import Grade

User = get_user_model()

class GradeAPITest(APITestCase):
    def setUp(self):
        self.teacher_user = User.objects.create_user(username='teacher', password='teacherpass', role='teacher')
        self.student_user = User.objects.create_user(username='student', password='studentpass', role='student')
        self.student = Student.objects.create(user=self.student_user, dob="2000-01-01")
        self.course = Course.objects.create(name="Math", description="Basic Math", instructor=self.teacher_user)
        self.grade = Grade.objects.create(student=self.student, course=self.course, grade=95.5, teacher=self.teacher_user)

    def test_teacher_can_create_grade(self):
        self.client.login(username='teacher', password='teacherpass')
        response = self.client.post('/api/grades/', {
            'student': self.student.id,
            'course': self.course.id,
            'grade': 88.5,
            'teacher': self.teacher_user.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_grade(self):
        self.client.login(username='student', password='studentpass')
        response = self.client.post('/api/grades/', {
            'student': self.student.id,
            'course': self.course.id,
            'grade': 88.5,
            'teacher': self.teacher_user.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_grades(self):
        self.client.login(username='student', password='studentpass')
        response = self.client.get('/api/grades/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure one grade is returned
