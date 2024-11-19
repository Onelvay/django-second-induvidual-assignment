from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from courses.models import Course
from students.models import Student

User = get_user_model()

class CourseAPITest(APITestCase):
    def setUp(self):
        self.teacher_user = User.objects.create_user(username='teacher', password='teacherpass', role='teacher')
        self.student_user = User.objects.create_user(username='student', password='studentpass', role='student')

        self.course = Course.objects.create(
            name="Physics",
            description="Basic Physics Course",
            instructor=self.teacher_user
        )

    def test_teacher_can_create_course(self):
        self.client.login(username='teacher', password='teacherpass')
        response = self.client.post('/api/courses/', {
            'name': 'Math',
            'description': 'Basic Math Course',
            'instructor': self.teacher_user.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_course(self):
        self.client.login(username='student', password='studentpass')
        response = self.client.post('/api/courses/', {
            'name': 'Math',
            'description': 'Basic Math Course',
            'instructor': self.teacher_user.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_courses(self):
        self.client.login(username='student', password='studentpass')
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Убедимся, что курс отображается
