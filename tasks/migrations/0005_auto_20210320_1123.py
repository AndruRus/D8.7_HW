# Generated by Django 2.2.10 on 2021-03-20 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_prioritycount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='prioritycount',
            options={'verbose_name': 'Счетчик приоритетов', 'verbose_name_plural': 'Счетчик приоритетов'},
        ),
        migrations.AlterField(
            model_name='prioritycount',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]
