from django.http import HttpResponse, HttpResponseNotFound
from django.db import connection, ProgrammingError
from django.template import loader
from django.shortcuts import render, redirect

# Create your views here.

def masterPageFront(request):
    template = loader.get_template("masterPageFront.html")
    return HttpResponse(template.render())

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def kanban(request):
    template = loader.get_template("kanban.html")
    return HttpResponse(template.render())