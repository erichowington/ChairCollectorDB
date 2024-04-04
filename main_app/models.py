from django.db import models
from datetime import date
from django.contrib.auth.models import User

LOCATIONS = (
    ('PER', 'Personal'),
    ('MUS', 'Museum'),
    ('SHO', 'Shop')
)

CREDIT = (
    ('Y','YES'),
    ('N','NO')
)

class Dupe(models.Model):
    dupe_manufacturer = models.CharField('Dupe Manufacturer', max_length=100,)
    credits = models.CharField('Credit Given',
        max_length = 3,
        choices = CREDIT,
        default = CREDIT [0][0]
    )
    
    def __str__(self):
        return self.dupe_manufacturer


class Chair(models.Model):
    model = models.CharField(max_length=100)
    designer = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    release = models.IntegerField()
    dupes = models.ManyToManyField(Dupe)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.model
    

class Sightings(models.Model):
    date = models.DateField('Sighting Date')
    location = models.CharField(
        max_length = 3,
        choices = LOCATIONS,
        default = LOCATIONS[0][0]
    )
    chair = models.ForeignKey(Chair, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.get_location_display()} on {self.date}'
    class Meta:
        ordering = ['-date']
        

    
    