from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dis_list/', views.dis_list, name='dis_list'),
    path('symptoms_list/', views.symptoms_list, name='symptoms_list'),
    path('check_sym/', views.check_sym, name='check_sym'),
    path('check_disease/', views.check_disease, name='check_disease'),
]