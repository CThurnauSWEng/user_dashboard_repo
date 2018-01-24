from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),
    url(r'register$', views.register),
    url(r'create$', views.user_create),
    url(r'signin$', views.signin),
    url(r'login$', views.user_login),
    url(r'logout$', views.user_logout),
    url(r'welcome$', views.welcome),   
    url(r'manage$', views.manage),     
    url(r'users/new$', views.admin_add_new),   
    url(r'edit$', views.edit)    
]