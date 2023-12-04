from django.http import HttpResponse, HttpResponseNotFound
from django.db import connection, ProgrammingError
from django.template import loader
from django.shortcuts import render, redirect

# Create your views here.

def masterPagee(request):
    template = loader.get_template("masterPagee.html")
    return HttpResponse(template.render())

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())