from django.test import TestCase
from time_series.tests.models import TestTimeSeries, TestDatePoint
from django.conf import settings
import datetime
from django.core.management import call_command
from django.db.models import loading


class BasicInheritanceTest(TestCase):
    def setUp(self):
        self.OLD_INSTALLED_APPS = settings.INSTALLED_APPS
        settings.INSTALLED_APPS = (
            'time_series',
            'time_series.tests',
        )
        loading.cache.loaded = False
        call_command('syncdb', verbosity=0)

        self.ts = TestTimeSeries.objects.create()
        self.today = datetime.date.today()
        self.a = TestDatePoint.objects.create(
                data=5, name="first", date=self.today,
                time_series=self.ts)

    def tearDown(self):
        settings.INSTALLED_APPS = self.OLD_INSTALLED_APPS
        loading.cache.loaded = False
        call_command('syncdb', verbosity=0)

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

