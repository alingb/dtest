from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.base, name="disk_index"),
    url(r'adddisk/', views.diskAddInfo, name="disk_index"),
    url(r'disk_add/', views.diskAdd, name="disk_index"),
    url(r'disk_info/', views.diskInfo, name="disk_info"),
    url(r'file_info/', views.fileInfo, name="file_info"),
    url(r'file/(?P<id>.*)/', views.fileDetail, name="file_detail"),
    url(r'filemanger/', views.fileManger, name="file_manger"),
    url(r'createfile/', views.createFile, name="file_crete"),
    url(r'changefile/', views.changeFile, name="file_change"),
    url(r'changegroup/', views.gropupChange, name="group_change"),
    url(r'groupinfo/', views.groupInfo, name="group_info"),
    url(r'checkroute/', views.chechRoute, name="check_route"),
    url(r'diskback/', views.diskBack, name="disk_back"),
    url(r'change/', views.changeFileInfo, name="change"),
    url(r'changedata/', views.changeData, name="change_data"),
]