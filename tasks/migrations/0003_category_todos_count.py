# Generated by Django 2.2.10 on 2021-03-19 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20210319_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='todos_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]