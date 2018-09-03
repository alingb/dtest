from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.base, name="disk_index"),
    url(r'cpustat/$', views.cpuStat, name="disk_index"),
    url(r'memstat/$', views.memStat, name="disk_index"),
    url(r'diskstat/$', views.diskStat, name="disk_index"),
    url(r'netstat/(?P<netname>.*)$', views.netStat, name="disk_index"),
    url(r'get_info/(?P<getname>.*)/', views.get_info, name="web_get_info"),
]
