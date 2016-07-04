from django.shortcuts import render, get_object_or_404
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponseForbidden)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import loader

from . import models, forms


def home(request):
    codes = []
    if request.user.is_authenticated():
        codes = models.UserCode.objects.filter(owner=request.user)
    return render(request, 'home.html', {
        'title': 'Pode',
        'codes': codes
    })


def user_code(request, username, slug):
    # TODO: We *really* need to be serving this on a separate domain
    # to prevent rampant XSS.

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
                {
                    'title': title,
                    'username': request.user.username,
                    'home_url': request.build_absolute_uri(
                        reverse('pode:home')
                    )
                }
            )
            code.save()
            return HttpResponseRedirect(code.get_absolute_url())
    else:
        form = forms.CreateUserCodeForm()

    return render(request, 'create_user_code.html', {
        'title': 'Create a new HTML page',
        'form': form
    })


@login_required
def edit_user_code(request, username, slug):
    code = get_object_or_404(
        models.UserCode,
        owner__username=username,
        slug=slug
    )
    if code.owner != request.user and not code.is_staff:
        return HttpResponseForbidden()

    was_just_saved = False
    title = 'Edit HTML page'

    if request.method == 'POST':
        form = forms.EditUserCodeForm(request.POST, instance=code)
        if form.is_valid():
            form.save(commit=True)
            was_just_saved = True
            title = 'HTML page saved'
    else:
        form = forms.EditUserCodeForm(instance=code)

    return render(request, 'edit_user_code.html', {
        'title': title,
        'form': form,
        'username': username,
        'slug': slug,
        'share_url': code.get_absolute_url_for_sharing(request),
        'was_just_saved': was_just_saved
    })
