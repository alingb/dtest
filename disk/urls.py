from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.base, name="disk_index"),
    url(r'disk_info/', views.disk, name="disk_info"),
    url(r'filemanger/', views.fileManger, name="file_manger"),
    url(r'createfile/', views.createFile, name="file_crete"),
    url(r'changefile/', views.changeFile, name="file_change"),
    url(r'changegroup/', views.gropupChange, name="group_change"),
    url(r'groupinfo/', views.groupInfo, name="group_info"),

]