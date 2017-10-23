from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^product/(?P<pid>[0-9]+)/$', views.view_product, name='view_product'),
    url(r'^todaysorders/$', views.view_todays_orders, name='view_todays_orders'),
    url(r'^order/(?P<oid>[0-9]+)/$', views.view_orders, name='view_orders'),

]