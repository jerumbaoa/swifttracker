from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from django.conf import settings

class Profile(models.Model):
    POSITION = (('developer','developer'), ('designer','designer'))
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    position = models.CharField(max_length=120, choices=POSITION, default="")
    birthdate = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=120)
    

    def __str__(self):
        return str(self.user)

class Project(models.Model):
    POSITION = (('developer', 'developer'), ('designer', 'designer'))
    
    username = models.ManyToManyField(User)
    name = models.CharField(max_length=1000)
    position = models.CharField(max_length=1000, choices=POSITION)
    weekly_hours = models.IntegerField()


    def __str__(self):
        return "{}".format(self.name)

class WeeklyReport(models.Model):
    project_name = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=150)
    date_track = models.DateField()
    question1 = models.CharField(max_length=2000)
    question2 = models.CharField(max_length=2000)
    question3 = models.CharField(max_length=2000)
    time_track = models.CharField(max_length=2000)

    def __str__ (self):
        return "{}".format(self.time_track)
