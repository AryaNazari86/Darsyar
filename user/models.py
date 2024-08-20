from django.db import models

class User(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    
    PLATFORM_CHOICES = [
        ('TG', 'Telegram'),
        ('BALE', 'Bale'),
    ]
    
    platform = models.CharField(
        max_length=10,
        choices=PLATFORM_CHOICES,
        default='BALE',
    )

    id  = models.CharField(max_length=60, primary_key=True)#models.PositiveBigIntegerField(primary_key  = True)
    user_id = models.PositiveBigIntegerField(null  = True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    grade = models.ForeignKey(
        'content.Grade',
        on_delete=models.CASCADE,
        null = True,
    )

    is_student = models.BooleanField(default = 1)
    state = models.IntegerField(default=0)
    calculated_score = models.IntegerField(default = 0)

    date_created = models.DateTimeField(auto_now_add=True)

    inviter = models.ForeignKey(
        'user.User',
        related_name='invitee',
        on_delete=models.CASCADE,
        null = True
    )

    class Meta:
        unique_together = ('platform', 'user_id')

    def score(self):
        sc = 0
        for i in self.solved_questions.all():
            sc += i.point

        sc += self.invitee.count() * 1001
        
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
    