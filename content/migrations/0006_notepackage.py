# Generated by Django 4.1 on 2024-09-08 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0028_alter_user_last_name'),
        ('content', '0005_question_hint'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_id', models.CharField(max_length=100)),
                ('is_disabled', models.BooleanField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('platform', models.CharField(choices=[('TG', 'Telegram'), ('BALE', 'Bale')], default='BALE', max_length=10)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='user.user')),
                ('class_rel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='content.class')),
            ],
        ),
    ]
