from django.shortcuts import render


def home(request):
    return render(request, 'base.html', {
        'title': 'Welcome to Pode'
    })
