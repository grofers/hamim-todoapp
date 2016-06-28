from django.conf.urls import url
from tasks import views

urlpatterns = [
    url(r'^tasks/(?P<pk>[0-9]+)/$', views.modify_tasks),
    url(r'^tasks/', views.list_tasks),
    url(r'^users/$', views.list_users),
    url(r'^users/(?P<pk>[0-9]+)/$', views.modify_users),
]
