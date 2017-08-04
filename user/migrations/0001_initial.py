# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 10:42
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


def add_default_role_func(apps, schema_editor):
    Role = apps.get_model("user", "Role")
    db_alias = schema_editor.connection.alias
    Role.objects.using(db_alias).bulk_create([
        Role(name="学生",
             permission=("{checkin,school,school_classroom,school_classroom_view,school_schoolterm," +
                         "school_schoolterm_view,school_classtime,school_classtime_view}")),
        Role(name="教师",
             permission=("{course,course_viewlist,checkin,school,school_teacher,school_class,school_class_view," +
                         "school_major,school_major_view,school_department,school_department_view,school_department," +
                         "school_department_view,school_classroom,school_classroom_view,school_schoolterm," +
                         "school_schoolterm_view,school_classtime,school_classtime_view}")),
        Role(name="管理员",
             permission=("{course,course_viewlist,course_control,checkin,checkin_ask,checkin_ask_add," +
                         "checkin_ask_modify,checkin_ask_approve,checkin_view,checkin_modify,wechat,wechat_control," +
                         "user,user_viewlist,user_modify,user_addrole,user_addpermission,school,school_student," +
                         "school_student_view,school_student_modify,school_teacher,school_teacher_view,school_class," +
                         "school_class_view,school_major,school_major_view,school_department,school_department_view," +
                         "school_department,school_department_view,school_classroom,school_classroom_view," +
                         "school_schoolterm,school_schoolterm_view,school_schoolterm_modify,school_classtime," +
                         "school_classtime_view,school_classtime_modify}")),
        Role(name="助教",
             permission=("{checkin,school,school_student,school_student_view,school_teacher,school_teacher_view," +
                         "school_class,school_class_view,school_major,school_major_view,school_department," +
                         "school_department_view,school_department,school_department_view,school_classroom," +
                         "school_classroom_view,school_schoolterm,school_schoolterm_view,school_classtime," +
                         "school_classtime_view}")),
        Role(name="教秘",
             permission=("{course,course_viewlist,checkin,checkin_ask,checkin_ask_add,checkin_ask_modify," +
                         "checkin_ask_approve,checkin_view,user,user_viewlist,school,school_student," +
                         "school_student_view,school_teacher,school_teacher_view,school_class,school_class_view," +
                         "school_major,school_major_view,school_department,school_department_view,school_department" +
                         ",school_department_view,school_classroom,school_classroom_view,school_schoolterm," +
                         "school_schoolterm_view,school_classtime,school_classtime_view}")),
        Role(name="校长",
             permission=("{course,course_viewlist,checkin,checkin_ask,checkin_ask_add,checkin_ask_modify," +
                         "checkin_ask_approve,checkin_view,user,user_viewlist,school,school_student," +
                         "school_student_view,school_teacher,school_teacher_view,school_class,school_class_view," +
                         "school_major,school_major_view,school_department,school_department_view,school_department," +
                         "school_department_view,school_classroom,school_classroom_view,school_schoolterm," +
                         "school_schoolterm_view,school_classtime,school_classtime_view}")),
        Role(name="教务处",
             permission=("{course,course_viewlist,course_control,checkin,checkin_ask,checkin_ask_add," +
                         "checkin_ask_modify,checkin_ask_approve,checkin_view,checkin_modify,wechat,wechat_control," +
                         "user,user_viewlist,user_modify,school,school_student,school_student_view," +
                         "school_student_modify,school_teacher,school_teacher_view,school_class,school_class_view," +
                         "school_major,school_major_view,school_department,school_department_view,school_department," +
                         "school_department_view,school_classroom,school_classroom_view,school_schoolterm," +
                         "school_schoolterm_view,school_schoolterm_modify,school_classtime,school_classtime_view," +
                         "school_classtime_modify}")),
    ])


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('permission',
                 django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True,
                                                           default=[], size=None)),
            ],
            options={
                'db_table': 'Role',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('academiccode', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('openid', models.CharField(blank=True, max_length=28, null=True, unique=True)),
                ('wechatdeviceid', models.CharField(blank=True, max_length=32, null=True)),
                ('password', models.CharField(blank=True, max_length=32, null=True)),
                ('sex', models.IntegerField(blank=True, default=1, null=True)),
                ('ip', models.GenericIPAddressField(blank=True, null=True, protocol=b'IPv4')),
                ('lastlogintime', models.DateTimeField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=40, null=True, unique=True)),
                ('avatar', models.ImageField(default=b'avatar/default.png', upload_to=b'avatar')),
                ('checkinaccountabnormal', models.BooleanField(default=False)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('accuracy', models.FloatField(blank=True, null=True)),
                ('lastpositiontime', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='Usertorole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(blank=True, db_column=b'roleid', null=True,
                                           on_delete=django.db.models.deletion.DO_NOTHING, to='user.Role')),
                ('user', models.ForeignKey(blank=True, db_column=b'userid', null=True,
                                           on_delete=django.db.models.deletion.DO_NOTHING, to='user.User')),
            ],
            options={
                'db_table': 'UsertoRole',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ManyToManyField(through='user.Usertorole', to='user.Role'),
        ),
        migrations.AlterUniqueTogether(
            name='usertorole',
            unique_together=set([('user', 'role')]),
        ),
        migrations.RunPython(add_default_role_func),
    ]
