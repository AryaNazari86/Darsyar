from django.db import models

class User(models.Model):
    user_id  = models.PositiveBigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    grade = models.ForeignKey(
        'content.Grade',
        on_delete=models.CASCADE,
        null = True,
    )
    state = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


