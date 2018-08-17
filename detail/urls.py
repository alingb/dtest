from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="detail"),
    url(r'detail/$', views.produceDetail, name="productDetail"),
    url(r'change/$', views.change, name="change"),

]
