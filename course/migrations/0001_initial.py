# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 10:42
from __future__ import unicode_literals

import course.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serialnumber', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('number', models.SmallIntegerField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('time', models.CharField(blank=True, max_length=400, null=True)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('schoolterm', models.CharField(blank=True, max_length=20, null=True)),
                ('department', models.ForeignKey(blank=True, db_column=b'departmentid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='school.Department')),
                ('major', models.ForeignKey(blank=True, db_column=b'majorid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='school.Major')),
                ('teachclass', models.ForeignKey(blank=True, db_column=b'teachclassid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='school.Class')),
                ('teachers', models.ManyToManyField(to='school.Teacher')),
            ],
            options={
                'db_table': 'Course',
            },
        ),
        migrations.CreateModel(
            name='Coursehomework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('instruction', models.TextField(blank=True, null=True)),
                ('type', models.SmallIntegerField(blank=True, null=True)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('weight', models.SmallIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'CourseHomework',
            },
        ),
        migrations.CreateModel(
            name='Courseresource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('uploadtime', models.DateTimeField(blank=True, null=True)),
                ('file', models.FileField(upload_to=course.models.get_courseresource_path)),
                ('course', models.ForeignKey(blank=True, db_column=b'courseid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='course.Course')),
            ],
            options={
                'db_table': 'CourseResource',
            },
        ),
        migrations.CreateModel(
            name='Homeworkcommit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submittime', models.DateTimeField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('score', models.SmallIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'HomeworkCommit',
            },
        ),
        migrations.CreateModel(
            name='Homeworkfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('file', models.FileField(upload_to=b'homeworkfile')),
            ],
            options={
                'db_table': 'HomeworkFile',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.SmallIntegerField(blank=True, null=True)),
                ('status', models.SmallIntegerField(blank=True, null=True)),
                ('year', models.SmallIntegerField(blank=True, null=True)),
                ('term', models.CharField(blank=True, max_length=20, null=True)),
                ('week', models.SmallIntegerField(blank=True, null=True)),
                ('time', models.SmallIntegerField(blank=True, null=True)),
                ('day', models.SmallIntegerField(blank=True, null=True)),
                ('starttime', models.DateTimeField(blank=True, null=True)),
                ('endtime', models.DateTimeField(blank=True, null=True)),
                ('checkincount', models.SmallIntegerField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('classroom', models.ForeignKey(blank=True, db_column=b'classroomid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='school.Classroom')),
                ('course', models.ForeignKey(blank=True, db_column=b'courseid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='course.Course')),
            ],
            options={
                'db_table': 'Lesson',
            },
        ),
        migrations.CreateModel(
            name='Studentcourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(blank=True, db_column=b'courseid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='courses', to='course.Course')),
                ('student', models.ForeignKey(blank=True, db_column=b'studentid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='school.Student')),
            ],
            options={
                'db_table': 'StudentCourse',
            },
        ),
        migrations.AddField(
            model_name='homeworkcommit',
            name='attachment',
            field=models.ManyToManyField(to='course.Homeworkfile'),
        ),
        migrations.AddField(
            model_name='homeworkcommit',
            name='coursehomework',
            field=models.ForeignKey(blank=True, db_column=b'coursehomeworkid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='course.Coursehomework'),
        ),
        migrations.AddField(
            model_name='homeworkcommit',
            name='student',
            field=models.ForeignKey(blank=True, db_column=b'studentid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='school.Student'),
        ),
        migrations.AddField(
            model_name='coursehomework',
            name='attachment',
            field=models.ManyToManyField(to='course.Homeworkfile'),
        ),
        migrations.AddField(
            model_name='coursehomework',
            name='course',
            field=models.ForeignKey(blank=True, db_column=b'courseid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='course.Course'),
        ),
        migrations.AlterUniqueTogether(
            name='studentcourse',
            unique_together=set([('student', 'course')]),
        ),
        migrations.AlterUniqueTogether(
            name='homeworkcommit',
            unique_together=set([('coursehomework', 'student')]),
        ),
    ]
