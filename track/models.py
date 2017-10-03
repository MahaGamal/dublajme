# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Track(models.Model):
    track_name = models.CharField(max_length=30)
    dublaj_url = models.CharField(max_length=200)
    origin_url = models.CharField(max_length=200)
    approve    = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')
    course = models.ForeignKey('track.course', null=True, blank=True)

class Course(models.Model):
    name = models.CharField('Course Name', max_length=200)
    category = models.CharField('Course Category', max_length=200, choices=[('tech','Technical'), ('eco', 'Economy'), ('art', 'Art')])
    base_url = models.URLField('Base URL')
    image = models.FileField('Course Thumbnail')
    source = models.CharField('MOOC', max_length=200, choices=[('udemy', 'udemy'), ('coursera', 'coursera'), ('udacity', 'udacity'), ('edx', 'edx')])
    price = models.IntegerField()
    list_price=models.IntegerField()
    duration = models.FloatField()

    # def save(self, *args, **kwargs):
    #     # For automatic set false .
    #     if not self.approve:
    #         self.approve = false

    #     return super(Track, self).save(*args, **kwargs)

