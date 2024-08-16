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

    def count_questions(self):
        counter = 0
        for unit in self.units.all():
            counter += unit.questions.count()
        return counter

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=100)
    class_rel = models.ForeignKey(
        "content.Class",
        on_delete=models.CASCADE,
        related_name="units"
    )

    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.TextField()
    answer = models.TextField(null=True)
    hint = models.TextField(null=True)
    unit = models.ForeignKey(
        'content.Unit',
        related_name="questions",
        on_delete=models.CASCADE,
        null = True
    )
    source = models.ForeignKey(
        'content.Source',
        on_delete=models.CASCADE,
        related_name='questions',
        null = True,
    )

    def __str__(self): 
        return f"Question #{self.id}-#{self.unit.id}-#{self.unit.class_rel.id}"


class Source(models.Model):
    name = models.CharField(max_length = 100)
    url = models.URLField(null=True)

    def __str__(self):
        return self.name
