# Generated by Django 4.1 on 2024-08-14 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_user_is_student_alter_userquestionrel_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='calculated_score',
            field=models.IntegerField(default=0),
        ),
    ]
