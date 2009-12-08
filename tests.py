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

class InheritanceTest(TestCase):
    def setUp(self):
        self.ts = TestTimeSeries.objects.create()
        self.a = self.ts.add(
                data=5, name="first", date=datetime.date.today())
        print 'success'

    def testFirst(self):
        self.assertEqual(self.ts.first, self.a)

    def testCanonical(self):
        self.assertEqual(self.ts.canonical, self.a)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

