from django.shortcuts import redirect
from django.conf import settings


def environment_required(function):
    def wrap(request, *args, **kwargs):
        if request.session.get('environment') in settings.APP_ENVIRONMENTS:
            return function(request, *args, **kwargs)
        else:
            return redirect('environment')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

