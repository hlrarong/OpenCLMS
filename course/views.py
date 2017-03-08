# -*- coding: utf-8 -*-
import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from course.auth import has_course_permission
from models import Course, Lesson, Studentcourse, Courseresource
from user.auth import permission_required
from school.function import getCurrentSchoolYearTerm
import time


def information(request, courseid):
    coursedata = Course.objects.get(id=courseid)
    lessondata = Lesson.objects.filter(course=coursedata).order_by('week', 'day', 'time').all()
    return render(request, 'information.html',
                  {'coursedata': coursedata, 'lessondata': lessondata,
                   'courseperms': has_course_permission(request.user, coursedata)})


@permission_required(permission='course_viewlist')
def list(request):
    return render(request, 'list.html', {'term': getCurrentSchoolYearTerm()})


@permission_required(permission='course_viewlist')
def data(request):
    order = request.GET['order']
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    # lessondata = Lesson.objects.all()[offset: (offset + limit)]
    sort = request.GET.get('sort', '')
    if not sort == '':
        if order == "asc":
            coursedata = Course.objects.order_by(sort)
        else:
            coursedata = Course.objects.order_by("-%s" % sort)
    else:
        coursedata = Course.objects
    schoolterm = request.GET.get('schoolterm', default=None)
    if schoolterm:
        coursedata = coursedata.filter(schoolterm=schoolterm)
    major = request.GET.get('major', '')
    if not major == '':
        if major[:1] == '*':
            coursedata = coursedata.filter(department__name=major[1:])
        else:
            coursedata = coursedata.filter(major__name=major)
    search = request.GET.get('search', '')
    if not search == '':
        count = coursedata.filter(
            (Q(title__icontains=search) | Q(teacher__name__icontains=search)) | Q(serialnumber=search)
        ).count()
        coursedata = coursedata.select_related('teacher').select_related('major').select_related(
            'department').filter(
            (Q(title__icontains=search) | Q(teacher__name__icontains=search)) | Q(serialnumber=search)
        )[offset: (offset + limit)]
    else:
        count = coursedata.count()
        coursedata = coursedata.select_related('teacher').select_related('major').select_related(
            'department').all()[offset: (offset + limit)]

    rows = []
    for p in coursedata:
        ld = {'id': p.id, 'serialnumber': p.serialnumber, 'title': p.title, 'number': p.number,
              'schoolterm': p.schoolterm, 'time': p.time, 'location': p.location, 'teacher': p.teacher.name,
              'major': (p.major and [p.major.name] or [None])[0], 'department': p.department.name}
        rows.append(ld)
    data = {'total': count, 'rows': rows}
    return HttpResponse(json.dumps(data), content_type="application/json")


def studentcourse(request, courseid):
    coursedata = Course.objects.get(id=courseid)
    students = Studentcourse.objects.filter(course=coursedata).select_related('student', 'student__classid',
                                                                              'student__classid__major',
                                                                              'student__classid__department').all()
    return render(request, 'studentcourse.html',
                  {'coursedata': coursedata, 'students': students,
                   'courseperms': has_course_permission(request.user, coursedata)})


def resource(request, courseid):
    coursedata = Course.objects.get(id=courseid)
    resources = Courseresource.objects.filter(course=coursedata).all()
    resources.order_by('uploadtime')
    return render(request, 'resource.html',
                  {'coursedata': coursedata, 'courseperms': has_course_permission(request.user, coursedata),
                   'resources': resources})


def resourceupload(request):
    coursedata = Course.objects.get(id=request.POST.get('courseid'))
    if not has_course_permission(request.user, coursedata):
        return HttpResponse(json.dumps({'error':u'没有权限上传到此课程'}), content_type="application/json")
    res = Courseresource(course=coursedata, uploadtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    res.file = request.FILES['file_data']
    res.title = res.file.name
    res.save()
    deleteurl = reverse('course:resourcedelete', args=[])
    data = {
        'initialPreview': ["<h2><i class='glyphicon glyphicon-file'></i></h2>"],
        'initialPreviewConfig': [
            {
                'caption': res.title,
                'url': deleteurl,
                'key': res.id
            },
        ]
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


def resourcedelete(request):
    key = request.POST.get('key')
    res = Courseresource.objects.get(id=key)
    if not has_course_permission(request.user, res.course):
        return HttpResponse(json.dumps({'error':u'没有权限删除此课程文件'}), content_type="application/json")
    res.file.delete()
    res.delete()
    return HttpResponse(json.dumps([]), content_type="application/json")
