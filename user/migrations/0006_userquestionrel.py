# Generated by Django 4.1 on 2024-07-19 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_source_question_source'),
        ('user', '0005_user_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserQuestionRel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='content.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solved_questions', to='user.user')),
            ],
            options={
                'unique_together': {('user', 'question')},
            },
        ),
    ]
