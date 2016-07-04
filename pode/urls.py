from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'(?P<username>[a-zA-Z0-9\-]+)/(?P<slug>[a-zA-Z0-9\-]+)$',
        views.user_code, name='user_code'),
]
