# Generated by Django 4.1 on 2024-07-16 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_class_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='class_rel',
        ),
        migrations.AlterField(
            model_name='class',
            name='grades',
            field=models.ManyToManyField(related_name='classes', to='content.grade'),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_rel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='content.class')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='content.unit'),
        ),
    ]
