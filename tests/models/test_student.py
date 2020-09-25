from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized
import re

from equilizer.models import Student
from equilizer.validators import StudentValidator


class StudentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="student", password="password", email="student@test.edu"
        )
        self.user.save()

    @parameterized.expand(["11111111", "a1132a", "asdfjkl"***REMOVED***)
    def test_bad_student_id_fails_validation(self, id):
        ***REMOVED***
        Test that invalid student IDs don't pass when we clean the model
        ***REMOVED***
        with self.assertRaises(ValidationError):
            student = Student.objects.create(user=self.user, student_id=id)
            student.full_clean()
            student.save()

    @parameterized.expand(["111111", "212345", "000000"***REMOVED***)
    def test_good_student_id(self, id):
        ***REMOVED***
        Test that valid student IDs are created
        ***REMOVED***
        student = Student.objects.create(user=self.user, student_id=id)
        student.full_clean()
        student.save()

        self.assertEqual(student.student_id, id)
