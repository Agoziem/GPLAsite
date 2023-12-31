# Generated by Django 2.2 on 2023-12-01 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student_Portal', '0002_auto_20231130_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='students_pin_and_id',
            name='Age',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='PrimaryResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FirstTest', models.CharField(blank=True, default='-', max_length=100, null=True)),
                ('SecondTest', models.CharField(blank=True, default='-', max_length=100, null=True)),
                ('Exam', models.CharField(blank=True, default='-', max_length=100, null=True)),
                ('Total_100', models.CharField(blank=True, default='-', max_length=100, null=True)),
                ('FirstTermTotal', models.CharField(blank=True, default='-', max_length=100, null=True)),
                ('Total_200', models.CharField(blank=True, default='-', max_length=100, null=True)),
                ('Grade', models.CharField(blank=True, default='-', max_length=100, null=True)),
                ('SubjectPosition', models.CharField(blank=True, default='-', max_length=100, null=True)),
                ('Remark', models.CharField(blank=True, default='-', max_length=100, null=True)),
                ('Subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student_Portal.Subject')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student_Portal.Students_Pin_and_ID')),
                ('student_class', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='Student_Portal.Class')),
                ('students_result_summary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Student_Portal.Student_Result_Data')),
            ],
        ),
    ]
