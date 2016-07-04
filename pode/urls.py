from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^new$', views.create_user_code, name='create_user_code'),
    url(r'^(?P<username>[a-zA-Z0-9\-]+)/(?P<slug>[a-zA-Z0-9\-]+)$',
        views.user_code, name='user_code'),
    url(r'^(?P<username>[a-zA-Z0-9\-]+)/(?P<slug>[a-zA-Z0-9\-]+)/edit$',
        views.edit_user_code, name='edit_user_code'),
]
