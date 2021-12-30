from django.shortcuts import redirect
from django.conf import settings
from portal.models import Environment


def environment_required(function):
    def wrap(request, *args, **kwargs):
        env = request.session.get('environment')
        if Environment.objects.filter(name=env).exists():
            return function(request, *args, **kwargs)
        else:
            return redirect('environment')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
