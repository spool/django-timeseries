"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from time_series.tests.models import *
import datetime

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

class BasicInheritanceTest(TestCase):
    def setUp(self):
        self.ts = TestTimeSeries.objects.create()
        self.today = datetime.date.today()
        self.a = TestDatePoint.objects.create(
                data=5, name="first", date=self.today,
                time_series=self.ts)

    def testFirst(self):
        self.assertEqual(self.ts.first, self.a)

    def testLast(self):
        self.assertEqual(self.ts.last, self.a)

    def testCanonical(self):
        self.assertEqual(self.ts.canonical, self.a)

    def testStartDate(self):
        self.assertEqual(self.ts.start_date, self.today)

    def testEndDate(self):
        self.assertEqual(self.ts.end_date, self.today)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

