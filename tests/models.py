from django.db import models
from time_series.models import *

class TestTimeSeries(TimeSeries):
    """ Testing Time Series Class """

class TestDatePoint(DatePointCanonical):
    """ Testing datepoint class """
    data = models.IntegerField()
    name = models.CharField(max_length=50)
    time_series = models.ForeignKey('TestTimeSeries', null=True, 
            related_name='time_series')

    def __unicode__(self):
        return '%d %s' % (self.data, self.date)

