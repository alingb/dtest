from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.base, name="disk_index"),
    url(r'cpustat/$', views.cpuStat, name="cpu_stat"),
    url(r'memstat/$', views.memStat, name="mem_stat"),
    url(r'diskstat/$', views.diskStat, name="disk_stat"),
    url(r'log/$', views.logStat, name="log_info"),
    url(r'netstat/(?P<netname>.*)$', views.netStat, name="net_stat"),
    url(r'get_info/(?P<getname>.*)/', views.get_info, name="web_get_info"),
]
