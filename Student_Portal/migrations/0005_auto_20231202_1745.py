# Generated by Django 2.2 on 2023-12-02 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student_Portal', '0004_auto_20231202_1553'),
    ]

    operations = [
        migrations.RenameField(
            model_name='primaryresult',
            old_name='student',
            new_name='primary_student',
        ),
        migrations.RenameField(
            model_name='primaryresult',
            old_name='students_result_summary',
            new_name='primary_students_result_summary',
        ),
    ]
