# Generated by Django 4.1 on 2024-09-09 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0011_rename_downvote_notepackage_downvotes_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notepackage',
            old_name='is_disabled',
            new_name='confirmed',
        ),
    ]
