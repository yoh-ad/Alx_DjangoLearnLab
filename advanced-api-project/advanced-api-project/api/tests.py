# Note: included for completeness; main tests live in api/test_views.py
from django.test import TestCase

class SmokeTest(TestCase):
    def test_smoke(self):
        self.assertTrue(True)
