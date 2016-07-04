from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import loader

from . import models, forms


def home(request):
    return render(request, 'home.html', {
        'title': 'Pode'
    })


def user_code(request, username, slug):
    code = get_object_or_404(
        models.UserCode,
        owner__username=username,
        slug=slug
    )
    return HttpResponse(code.content)


@login_required
def create_user_code(request):
    if request.method == 'POST':
        form = forms.CreateUserCodeForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            code = models.UserCode.objects.create_from_title(
                owner=request.user,
                title=title
            )
            code.content = loader.render_to_string(
                'actual_user_code_templates/html.html',
                {'title': title}
            )
            code.save()
            return HttpResponseRedirect(code.get_absolute_url())
    else:
        form = forms.CreateUserCodeForm()

    return render(request, 'create_user_code.html', {
        'title': 'Create a new HTML page',
        'form': form
    })
