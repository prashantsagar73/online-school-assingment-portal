# Generated by Django 3.2 on 2021-04-12 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0005_assignmentcompleted_owner_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentcompleted',
            name='more',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='assignmentcompleted',
            name='score',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
    ]
