from django.db import models

# Create your models here.
class LOG(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)

    TYPES = (
        (0, 'Question'),
        (1, 'Test'),
        (2, 'AI'),
    )

    type = models.IntegerField(default=0, choices=TYPES)

    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="logs"
    )