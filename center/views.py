from django.shortcuts import render

from course.models import Studentcourse, Lesson, Course, Coursehomework, Homeworkcommit
from school.function import getCurrentSchoolYearTerm, getnowlessontime
from school.models import Student, Teacher


# Create your views here.
# @resourcejurisdiction_view_auth(jurisdiction='school')
def home(request):
    if request.user.isteacher:
        teacher = Teacher.objects.get(user=request.user)
        termcourse = teacher.course_set.filter(schoolterm=getCurrentSchoolYearTerm()['term'])
        uncommithomework = None
    else:
        student = Student.objects.get(user=request.user)
        # alreadycount = Checkin.objects.filter(studentid=student)
        # alreadycount.query.group_by = ['lessonruntimeid__lessonid__id']

        termcourse = Studentcourse.objects.filter(student=student, course__schoolterm=getCurrentSchoolYearTerm()[
            'term']).values_list('course', flat=True)
        termcourse = Course.objects.filter(id__in=termcourse)
        commithomework = Homeworkcommit.objects.filter(student=student).values_list('coursehomework', flat=True)
        uncommithomework = Coursehomework.objects.filter(course__in=termcourse).exclude(
            id__in=commithomework).select_related('course').all()

    nowlessontime = getnowlessontime()
    lesson = Lesson.objects.filter(course__in=termcourse, week=nowlessontime['week']).order_by('week', 'day', 'time')

    return render(request, 'home.html',
                  {'term': getCurrentSchoolYearTerm(),
                   'uncommithomework': uncommithomework,
                   'termcourse': termcourse.all(),
                   'weeklesson': lesson.select_related('course').select_related('classroom').all(),
                   })


def seat(request):
    return render(request, 'seat.html')
