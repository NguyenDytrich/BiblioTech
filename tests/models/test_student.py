from django.test import TestCase
from equilizer.models import Student
from parameterized import parameterized


class StudentTestCase(TestCase):
    @parameterized.expand(["11111111", "a1132a", "asdfjkl"***REMOVED***)
    def test_bad_student_id_fails_validation(self):
        self.fail("TODO")

    @parameterized.expand(["111111", "212345", "000000"***REMOVED***)
    def test_good_student_id(self):
        self.fail("TODO")
