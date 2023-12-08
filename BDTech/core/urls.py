from django.contrib import admin
from django.urls import path
from backend.views import  dashboard, generic_list, error404, delete_record
from frontend.views import  index, kanban, login_utilizador, logout_utilizador

urlpatterns = [
    path("", dashboard),
    path("404/", error404),
    path("<str:table_name>/list/", generic_list, name='generic_list'),
    path("index/", index),
    path("kanban/", kanban),
    path('delete_record/<str:table_name>/<int:record_id>/', delete_record, name='delete_record'),
    path('login/', login_utilizador, name='login'),
    path('logout/', logout_utilizador, name='logout'),
]
