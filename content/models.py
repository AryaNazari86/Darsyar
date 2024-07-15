from django.db import models

class Grade(models.Model):
    name = models.CharField(max_length = 100)
    grade_number = models.IntegerField()

    def __str__(self):
        return self.name
    
class Class(models.Model):
    name = models.CharField(max_length=100)
    grades = models.ManyToManyField(
        'content.Grade',
        related_name="classes"
    )
    grade_number = models.IntegerField()

class Question(models.Model):
    text = models.TextField()
    answer = models.TextField(null=True)
    class_rel = models.ForeignKey(
        'content.Class',
        related_name="questions",
        on_delete=models.CASCADE
    )
