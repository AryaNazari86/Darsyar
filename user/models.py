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

    def score(self):
        sc = 0
        for i in self.solved_questions.all():
            sc += i.point
        
        return sc
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserQuestionRel(models.Model):
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='solved_questions'
    )
    question = models.ForeignKey(
        'content.Question',
        on_delete=models.CASCADE,
        related_name='users',
    )
    point = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user} - {self.question}"