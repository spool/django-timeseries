from django.db import models
import datetime

class TimeSeries(models.Model):
    """
    Abstract Base class for aggregating time series.

    Requires a related time_series class.
    """
    @property
    def first(self):
        try:
            return self.time_series.order_by('nodefile__date')[0]
        except:
            pass

    @property
    def canonical(self):
        """
        Returns the canonical node from the time series
        which is determined by the is_canonical boolean if
        it exists, and defaults to the first object in the
        series if it does not.
        
        Raises a MultipleCanonicalError if multiple objects
        have is_canonical = True

        TODO use get instead and standard get execptions.
        """
        try:
            return self.time_series.get(is_canonical=True)
        except ObjectDoesNotExist:
            print "WARNING: %s has no canonical time point." % self.first
        except MultipleObjectsReturned:
            raise self.MultipleCanonicalError

    @property
    def last(self):
        try:
            return self.time_series.order_by('-nodefile__date')[0]
        except:
            pass

    @property
    def start_date(self):
        try:
            self.first.date
        except:
            pass

    @property
    def end_date(self):
        try:
            return self.last.date
        except:
            pass

    def date_range_qs(self, start_date=None, end_date=None):
        """
        Returns a queryset of state_change objects for given
        date range takes an optional start_date and end_date
        Assumes they are passed as datetime.date objects.
        """
        try:
            qs = self.time_series.all()
            if start_date:
                qs = qs.filter(date__gt=start_date)
            if end_date:
                qs = qs.filter(date__lt=end_date)
            return qs
        except:
            pass

    def __unicode__(self):
        try:
            return self.canonical
        except:
            return 'id: %d' % self.id

    def MultipleCanonicalError(Exception):
        """Raised when time series has more than one canonical time point.

        TODO: Make time series issue warning.
        """
        print "Multiple Canonical Error"

    class Meta:
        abstract = True

class DatePointCanonical(models.Model):
    is_canonical = models.BooleanField(default=False)
    date = models.DateField()

    def get_next(self):
        """ Returns the next DatePoint or None if the last in the series.

        TODO: implement
        """
        pass

    def get_previous(self):
        """ Returns the next DatePoint or None if the last in the series.

        TODO: implement
        """
        pass

    class Meta:
        ordering = ['date']

'''
class GenericNodeTimePoint(models.Model):

    raw_data = models.CharField(max_length=500)
    nodefile = models.ForeignKey("NodeFile",
                                 related_name="time_series_set")

    name = models.CharField(max_length=200, blank=True)
    sysop = models.ForeignKey("Sysop", blank=True, null=True)

    number = models.PositiveIntegerField()

    coordinates = models.PointField(null=True, blank=True)
    phone_numbers = models.ManyToManyField("PhoneNumber",
         related_name="node_time_points", blank=True, null=True)
    phone_number_text = models.CharField(max_length = 40, blank=True)

    #region information
    # NB: State can be a country or US state or province
    region = models.CharField(max_length=100, blank=True) 
    city = models.CharField(max_length=100, blank=True)

    speeds = models.ManyToManyField("NodeSpeed", blank=True, null=True)
    flags = models.ManyToManyField("NodeFlag", blank=True, null=True)
    flags_text = models.CharField(max_length=1000, blank=True)

    connections = models.ManyToManyField("NodeTimePoint",
            blank=True, null=True)

    objects = models.GeoManager()

    @classmethod
    def is_net(cls):
        return cls is NetTimePoint

    @classmethod
    def is_zone(cls):
        return cls is ZoneTimePoint

    @classmethod
    def is_node(cls):
        return cls is NodeTimePoint

    @property
    def parent(self):
        if self.is_zone():
            return None
        elif self.is_node():
            return self.net
        else:
            if not self.parent_net:
                return self.zone
            else:
                return self.parent_net


    def hours(self):
        """
        Will eventually parse the state_text field to
        calculate the hours active per unit time.
        """
        pass

    @property
    def date(self):
        """
        Returns date from related NodeFile.
        """
        return self.nodefile.date

    @property
    def year(self):
        """
        Returns year from related NodeFile.
        """
        return self.date.year

    @property
    def day(self):
        """
        Returns the day of the related nodefile.
        """
        return self.nodefile.day

    def check_coordinates(self):
        """
        Returns true if the phone number may yield a valid coordinate
        pair.

        FIX
        """
        if self.phone_number:
            if self.zone:
                if self.zone == Zone.objects.get(number=1):
                    return True
                else:
                    return False
            return True

    def has_coordinates(self):
        if self.coordinates: return True
        else: return False

    def __unicode__(self):
        return "%s on day %s, %s" % \
                (self.name, self.day, self.year)

    class Meta:
        ordering = ['nodefile__date', 'number']
'''
