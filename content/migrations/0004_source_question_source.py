# Generated by Django 4.1 on 2024-07-19 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_remove_question_class_rel_alter_class_grades_unit_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='content.source'),
        ),
    ]
