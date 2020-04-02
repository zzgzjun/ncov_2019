from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'add/', views.add),
    url(r'add_city/', views.add_city),
    url(r'index/', views.index),
    url(r'', views.main),
    url(r'time/', views.time),
    url(r'image/', views.image),
    url(r'map/', views.get_map),
    url(r'insert_hotsearch/', views.insert_hotsearch),

]
