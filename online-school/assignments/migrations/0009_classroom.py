# Generated by Django 3.2 on 2021-04-12 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0008_auto_20210412_0809'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=100)),
            ],
        ),
    ]
