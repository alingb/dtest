from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.base),
    url(r'get_info/', views.get_info, name="web_get_info"),
]