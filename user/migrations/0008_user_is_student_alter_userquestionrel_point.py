# Generated by Django 4.1 on 2024-08-03 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_userquestionrel_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_student',
            field=models.BooleanField(default=1),
        ),
        migrations.AlterField(
            model_name='userquestionrel',
            name='point',
            field=models.IntegerField(default=0),
        ),
    ]
