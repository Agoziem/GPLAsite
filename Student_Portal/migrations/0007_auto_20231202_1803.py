# Generated by Django 2.2 on 2023-12-02 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student_Portal', '0006_auto_20231202_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='primaryresult',
            name='student',
        ),
        migrations.RemoveField(
            model_name='primaryresult',
            name='student_class',
        ),
        migrations.RemoveField(
            model_name='result',
            name='student',
        ),
        migrations.RemoveField(
            model_name='result',
            name='student_class',
        ),
    ]