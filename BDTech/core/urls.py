from django.contrib import admin
from django.urls import path
from backend.views import  dashboard, generic_list, error404
from frontend.views import  index, kanban

urlpatterns = [
    path("", dashboard),
    path("404/", error404),
    path("<str:table_name>/list/", generic_list, name='generic_list'),
    path("index/", index),
    path("kanban/", kanban),
]
