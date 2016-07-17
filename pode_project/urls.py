"""pode_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required, user_passes_test


# http://stackoverflow.com/a/13186337
admin.site.login = login_required(admin.site.login)


@user_passes_test(lambda u: u.is_superuser)
def throw_error_to_manually_test_logging(request):
    '''
    Because Django's logging configuration is the most confusing thing
    I have ever used, we'll use this endpoint to manually ensure that
    logging works.
    '''

    this_nonexistent_function_is_being_called_to_test_django_error_logging()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('github.urls', namespace='github')),
    url(r'^500$', throw_error_to_manually_test_logging),
    url(r'', include('pode.urls', namespace='pode')),
]
