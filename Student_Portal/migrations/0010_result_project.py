# Generated by Django 2.2 on 2023-12-03 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student_Portal', '0009_auto_20231203_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='Project',
            field=models.CharField(blank=True, default='-', max_length=100, null=True),
        ),
    ]
