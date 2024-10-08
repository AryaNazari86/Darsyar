# Generated by Django 4.1 on 2024-08-14 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_user_is_student_alter_userquestionrel_point'),
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='user.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='log',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
