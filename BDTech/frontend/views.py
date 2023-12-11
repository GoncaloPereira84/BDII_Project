from django.http import HttpResponse, HttpResponseNotFound
from django.db import connection, ProgrammingError
from django.template import loader
from django.shortcuts import render, redirect
from .models import Equipamento

# Create your views here.

def masterPageFront(request):
    template = loader.get_template("masterPageFront.html")
    return HttpResponse(template.render())

def index(request):
    ultimos_equipamentos = Equipamento.objects.order_by('id_equipamento')[:6]
    marcas = [
        {'nome': 'Apple', 'logo_url': 'https://th.bing.com/th/id/R.24e62b73004a5fb7a7a5d9c26963ed07?rik=nzIAxmu0duWlgA&riu=http%3a%2f%2fwww.zdnet.de%2fwp-content%2fuploads%2f2013%2f05%2fapple-logo-schwarz.jpg&ehk=q59%2b69Oq6FABvF0DbfJTGBD7m4IqvKMyNFPSzy8pRRg%3d&risl=&pid=ImgRaw&r=0'},
        {'nome': 'Lenovo', 'logo_url': 'https://th.bing.com/th/id/OIP.IRDIAwBmlFyff6g1EuFjXwHaEZ?rs=1&pid=ImgDetMain'},
        {'nome': 'Asus', 'logo_url': 'https://th.bing.com/th/id/OIP.M78UplVnuECVc6nFgq8p1wHaFj?w=640&h=480&rs=1&pid=ImgDetMain'},
        {'nome': 'MSI', 'logo_url': 'https://th.bing.com/th/id/OIP.S9Dvja4R5tcjaPYe381o0gHaEK?rs=1&pid=ImgDetMain'},
       

    ]
    return render(request, 'index.html', {'equipamentos': ultimos_equipamentos, 'marcas': marcas})

def kanban(request):
    template = loader.get_template("kanban.html")
    return HttpResponse(template.render())






