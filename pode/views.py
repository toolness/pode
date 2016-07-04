from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from . import models


def home(request):
    return render(request, 'base.html', {
        'title': 'Welcome to Pode'
    })


def user_code(request, username, slug):
    code = get_object_or_404(
        models.UserCode,
        owner__username=username,
        slug=slug
    )
    return HttpResponse(code.content)
