# Generated by Django 3.2 on 2021-04-12 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0007_rename_assignment_id_assignmentcompleted_assignment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='body',
            new_name='more',
        ),
        migrations.RenameField(
            model_name='assignmentcompleted',
            old_name='date_submited',
            new_name='date_created',
        ),
    ]
