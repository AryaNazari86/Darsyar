from django.db import models

class User(models.Model):
    user_id  = models.PositiveBigIntegerField(primary_key=True)
    grade = models.ForeignKey(
        'content.Grade',
        on_delete=models.CASCADE
    )


