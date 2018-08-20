from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="control"),
    url(r'ret/$', views.ret_show, name="control_ret"),
]
