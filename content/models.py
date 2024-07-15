from django.db import models

class Grade(models.Model):
    name = models.CharField(max_length = 100)
    grade_number = models.IntegerField()

    def __str__(self):
        return self.name
    
