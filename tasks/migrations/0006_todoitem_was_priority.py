# Generated by Django 2.2.10 on 2021-03-20 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20210320_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='was_priority',
            field=models.SmallIntegerField(default=0),
        ),
    ]
