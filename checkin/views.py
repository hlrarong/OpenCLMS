# coding:utf-8
from course.models import Lesson, Studentcourse, Course
from models import Checkin, Checkinrecord
from school.models import Student
from constant import *
from django.shortcuts import render_to_response, RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from course.constant import *
from checkin.function import clear_checkin, clear_last_checkin
import json


def checkin(request, lessonid):
    lesson = Lesson.objects.get(id=lessonid)
    if not (
                        lesson.status == LESSON_STATUS_CHECKIN or lesson.status == LESSON_STATUS_CHECKIN_AGAIN or lesson.status == LESSON_STATUS_CHECKIN_ADD):
        return render_to_response('error.html',
                                  {'message': '签到还未开始',
                                   'submessage': lesson.course.title,
                                   'jumpurl': str(
                                       reverse('course:information', args=[lesson.course.id]))},
                                  context_instance=RequestContext(request))
    if request.GET.get('deleteall', 0):
        clear_checkin(lessonid)
        return redirect(reverse('course:information', args=[lesson.course.id]))
    if request.GET.get('deletethis', 0):
        clear_last_checkin(lessonid)
        return redirect(reverse('course:information', args=[lesson.course.id]))
    studentlist = Studentcourse.objects.filter(course=lesson.course).all()
    data = {'lessondata': lesson, 'studentlist': studentlist}
    if lesson.status == LESSON_STATUS_CHECKIN_ADD:
        data['checkintype'] = u'补签'
    elif lesson.status == LESSON_STATUS_CHECKIN_AGAIN:
        data['checkintype'] = u'再签'
    return render_to_response('checkin.html', data,
                              context_instance=RequestContext(request))


def lesson_data(request, lessonid):
    lesson = Lesson.objects.get(id=lessonid)
    t = {'lessondata': lesson}
    if lesson.status == LESSON_STATUS_CHECKIN or lesson.status == LESSON_STATUS_CHECKIN_AGAIN or lesson.status == LESSON_STATUS_CHECKIN_ADD:
        return redirect(reverse('checkin:qrcheckin', args=[lessonid]))
    checkinrecord = Checkinrecord.objects.filter(lesson=lesson)
    checkincount = checkinrecord.count()
    t['checkincount'] = checkincount
    if not checkincount == 0:
        checkinrecord = checkinrecord.order_by('time').all()
        t['checkinrecord'] = checkinrecord

    return render_to_response('lesson_data.html', t, context_instance=RequestContext(request))


def course_data(request, courseid):
    course = Course.objects.get(id=courseid)
    alllesson = Lesson.objects.filter(course=course).exclude(status=LESSON_STATUS_AWAIT).order_by(
        'week',
        'day',
        'time').all()
    columns = [
        [{'field': 'name', 'title': u'学生', 'rowspan': 2, 'align': 'center', 'valign': 'middle', 'searchable': True},
         {'field': 'studentid', 'title': u'学号', 'rowspan': 2, 'align': 'center', 'valign': 'middle', 'searchable': True,
          'sortable': True},
         {'field': 'ratio', 'title': u'出勤率', 'rowspan': 2, 'align': 'center', 'valign': 'middle'},
         {'title': u'签到数据', 'colspan': alllesson.count(), 'align': 'center'}], []]
    # for i in range(0, count - 1):
    #    columns.append({'field': 'lesson%d' % i, 'title': i + 1, 'formatter': 'identifierFormatter'})
    for i, l in enumerate(alllesson):
        columns[1].append(
            {'field': 'lesson%d' % l.id, 'title': i + 1, 'formatter': 'identifierFormatter', 'align': 'center',
             'cellStyle': 'cellStyle'})
    studentdata = Studentcourse.objects.filter(course=course).order_by('student').all()
    lessoncheckindata = []
    '''for s in studentdata:
        studentcheckindata[s.student.studentid] = {'studentid': s.student.studentid, 'name': s.student.name}
    for l in alllesson:
        checkin = Checkin.objects.filter(lesson=l).all()
        for c in checkin:
    '''
    count = Checkin.objects.filter(lesson__course=course).distinct('lesson').count()
    for s in studentdata:
        studentcheckindata = {'studentid': s.student.studentid, 'name': s.student.name}
        checkindata = Checkin.objects.filter(student=s.student, lesson__course=course).order_by(
            'lesson__week',
            'lesson__day',
            'lesson__time').select_related(
            'lesson').all()
        ratio = 0.0
        for c in checkindata:
            studentcheckindata['lesson%d' % (c.lesson.id)] = c.status
            if c.status != 0:
                ratio += 1
        if count == 0:
            ratio = 1
        else:
            ratio = ratio / count
        studentcheckindata['ratio'] = '%.1f%%' % (ratio * 100)
        lessoncheckindata.append(studentcheckindata)
    print lessoncheckindata
    data = {'header': json.dumps(columns), 'newrows': json.dumps(lessoncheckindata)}
    return render_to_response('course_data.html', {'coursedata': course, 'data': data},
                              context_instance=RequestContext(request))


def student_data(request, studentid):
    student = Student.objects.get(studentid=studentid)
    studentcourse = Studentcourse.objects.filter(student=student).all()
    coursecount = studentcourse.count()
    course = {}
    maxlength = 0
    for sc in studentcourse:
        course[sc.course.id] = {'name': sc.course.title, 'courseid': sc.course.id, 'checkindata': {}}
        if sc.course.lesson_set.count() > maxlength:
            maxlength = sc.course.lesson_set.count()
        for (offset, l) in enumerate(sc.course.lesson_set.order_by('week', 'day', 'time').all()):
            course[sc.course.id]['checkindata'].update({l.id: {'status': None, 'offset': offset}})
    print course
    checkindata = Checkin.objects.filter(student=student).select_related('lesson').all()
    for c in checkindata:
        course[c.lesson.course.id]['checkindata'][c.lesson.id]['status'] = c.status

    rows = []
    for (k, v) in course.items():
        ld = {'courseid': v['courseid'], 'name': v['name']}
        # ld['data'] = []
        ratio = 0.0
        len = 0
        for (key, item) in v['checkindata'].items():
            if item['status'] != None:
                len += 1
                if item['status'] != 0:
                    ratio = ratio + 1
            ld.update({'lesson%d' % item['offset']: item['status']})
        if len == 0:
            ratio = 1
        else:
            ratio = ratio / len
        ld['ratio'] = '%.1f%%' % (ratio * 100)
        rows.append(ld)
    '''
    newrows = []
    for new in rows:
        a = {'name': new['name'], 'ratio': new['ratio']}
        for (offset, item) in enumerate(new['data']):
            a['lesson%d' % (offset)] = item
        newrows.append(a)
    print newrows
    '''

    columns = [
        [{'field': 'name', 'title': u'课程名称', 'rowspan': 2, 'align': 'center', 'valign': 'middle', 'searchable': True},
         {'field': 'ratio', 'title': u'出勤率', 'rowspan': 2, 'align': 'center', 'valign': 'middle'},
         {'title': u'签到数据', 'colspan': maxlength, 'align': 'center'}], []]

    for i in range(0, maxlength):
        columns[1].append(
            {'field': 'lesson%d' % i, 'title': i + 1, 'cellStyle': 'cellStyle', 'formatter': 'identifierFormatter',
             'align': 'center'})
    data = {'total': coursecount, 'rows': json.dumps(rows), 'header': json.dumps(columns)}
    return render_to_response('student_data.html', {'student': student, 'data': data},
                              context_instance=RequestContext(request))
