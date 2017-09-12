# -*- coding: utf-8 -*-
from functools import wraps
from django.shortcuts import render
from django.http import HttpResponse
import json


def permission_required(func=None, permission=None):
    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            user = request.user
            if user.has_perm(permission):
                return func(request, *args, **kwargs)
            else:
                if request.is_ajax():
                    return HttpResponse(json.dumps({'error': 101, 'message': '没有权限'}), content_type="application/json")
                else:
                    return render(request, 'error.html', {'message': '没有权限'})

        return returned_wrapper

    if not func:
        def foo(func):
            return decorator(func)

        return foo

    else:
        return decorator(func)
