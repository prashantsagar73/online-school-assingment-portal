# Generated by Django 3.2 on 2021-04-12 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0004_auto_20210412_0715'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentcompleted',
            name='owner_student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='assignments.student'),
        ),
    ]
