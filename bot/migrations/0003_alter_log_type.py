# Generated by Django 4.1 on 2024-08-17 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_log_user_alter_log_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='type',
            field=models.IntegerField(choices=[(0, 'Question'), (1, 'Test'), (2, 'AI'), (3, 'Hint')], default=0),
        ),
    ]
