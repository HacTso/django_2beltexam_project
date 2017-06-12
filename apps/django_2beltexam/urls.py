from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register_process),
    url(r'^login$', views.login_process),
    url(r'^quotes_process$', views.quotes_process),
    url(r'^quotes$', views.quotes),
    url(r'^logout$', views.logout),
]