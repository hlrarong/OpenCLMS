# coding=utf-8
from models import Lesson, Homeworkcommit
from constant import *
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
import json
from course.auth import has_course_permission


def startLesson(request):
    lessondata = Lesson.objects.get(id=request.GET.get('lessonid'))
    if not has_course_permission(request.user, lessondata.course):
        if request.is_ajax():
            return HttpResponse(json.dumps({'error': 101, 'message': '没有权限'}), content_type="application/json")
        else:
            return render(request, 'error.html',
                          {'message': '没有权限'})
    if request.is_ajax():
        return HttpResponse(json.dumps(lessondata.startlesson()), content_type="application/json")
    else:
        re = lessondata.startlesson()
        if re['error'] != 0:
            return render(request, 'error.html',
                          {'message': re['message'],
                           'submessage': lessondata.course.title,
                           'jumpurl': str(
                               reverse('course:information', args=[lessondata.course.id]))})
        else:
            if request.GET.get('jumptocheckin', default=0) == '1':
                return redirect(reverse('checkin:startcheckin', args=[lessondata.id]))
            else:
                return redirect(reverse('checkin:lesson_data', args=[lessondata.id]))


def stopLesson(request):
    lessondata = Lesson.objects.get(id=request.GET.get('lessonid'))
    if not has_course_permission(request.user, lessondata.course):
        if request.is_ajax():
            return HttpResponse(json.dumps({'error': 101, 'message': '没有权限'}), content_type="application/json")
        else:
            return render(request, 'error.html',
                          {'message': '没有权限'})
    if request.is_ajax():
        return HttpResponse(json.dumps(lessondata.stoplesson()), content_type="application/json")
    else:
        re = lessondata.stoplesson()
        if re['error'] != 0:
            return render(request, 'error.html',
                          {'message': re['message'],
                           'submessage': lessondata.course.title,
                           'jumpurl': str(
                               reverse('course:information', args=[lessondata.course.id]))})
        else:
            return redirect(reverse('course:information', args=[lessondata.course.id]))


def clearLesson(request):
    lessondata = Lesson.objects.get(id=request.GET.get('lessonid'))
    if not has_course_permission(request.user, lessondata.course):
        if request.is_ajax():
            return HttpResponse(json.dumps({'error': 101, 'message': '没有权限'}), content_type="application/json")
        else:
            return render(request, 'error.html',
                          {'message': '没有权限'})
    if request.is_ajax():
        return HttpResponse(json.dumps(lessondata.cleardata()), content_type="application/json")
    else:
        re = lessondata.cleardata()
        if re['error'] != 0:
            return render(request, 'error.html',
                          {'message': re['message'],
                           'submessage': lessondata.course.title,
                           'jumpurl': str(
                               reverse('course:information', args=[lessondata.course.id]))})
        else:
            return redirect(reverse('course:information', args=[lessondata.course.id]))


def sethomeworkscore(request):
    homeworkcommit = Homeworkcommit.objects.select_related('coursehomework').get(id=request.GET.get('homeworkcommitid'))
    score = request.GET.get('score')
    if not has_course_permission(request.user, homeworkcommit.coursehomework.course):
        return HttpResponse(json.dumps({'error': 101, 'message': '没有权限'}), content_type="application/json")
    homeworkcommit.score = score
    homeworkcommit.save()
    return HttpResponse(json.dumps({'error': 0, 'score': score, 'message': '评分成功'}), content_type="application/json")
