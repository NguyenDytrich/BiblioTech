from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized
import re

from library.models import Member
from library.validators import MemberValidator


class MemberTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="member", password="password", email="member@test.edu"
        )
        self.user.save()

    @parameterized.expand(["11111111", "a1132a", "asdfjkl"])
    def test_bad_student_id_fails_validation(self, id):
        """
        Test that invalid student IDs don't pass when we clean the model
        """
        with self.assertRaises(ValidationError):
            member = Member.objects.create(user=self.user, member_id=id)
            member.full_clean()
            member.save()

    @parameterized.expand(["111111", "212345", "000000"])
    def test_good_student_id(self, id):
        """
        Test that valid student IDs are created
        """
        member = Member.objects.create(user=self.user, member_id=id)
        member.full_clean()
        member.save()

        self.assertEqual(member.member_id, id)
