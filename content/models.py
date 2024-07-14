from django.db import models

class Grade(models.Model):
    grade_number = models.IntegerField()
    name = models.CharField(max_length = 100)
