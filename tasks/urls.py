from django.conf.urls import url
from tasks import views

urlpatterns = [
    url(r'^tasks/(?P<pk>[0-9]+)/$', views.modify_tasks),
    url(r'^tasks/$', views.tasks),
    url(r'^users/$', views.register),
    url(r'^users/session/$', views.login),
]
