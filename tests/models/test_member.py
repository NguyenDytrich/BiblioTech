from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized
import re

from bibliotech.models import Member
from bibliotech.validators import MemberValidator


class MemberTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="member", password="password", email="member@test.edu"
        )
        self.user.save()

    @parameterized.expand(["11111111", "a1132a", "asdfjkl"***REMOVED***)
    def test_bad_student_id_fails_validation(self, id):
        ***REMOVED***
        Test that invalid student IDs don't pass when we clean the model
        ***REMOVED***
        with self.assertRaises(ValidationError):
            member = Member.objects.create(user=self.user, member_id=id)
            member.full_clean()
            member.save()

    @parameterized.expand(["111111", "212345", "000000"***REMOVED***)
    def test_good_student_id(self, id):
        ***REMOVED***
        Test that valid student IDs are created
        ***REMOVED***
        member = Member.objects.create(user=self.user, member_id=id)
        member.full_clean()
        member.save()

        self.assertEqual(member.member_id, id)
