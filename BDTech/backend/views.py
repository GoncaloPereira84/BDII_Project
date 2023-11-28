from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Utilizador, Fornecedor

def masterPage(request):
  template = loader.get_template('masterPage.html')
  return HttpResponse(template.render())

def dashboard(request):
  template = loader.get_template('dashboard.html')
  return HttpResponse(template.render())

def utilizador_list(request):
    from django.db import connection
    c = connection.cursor()
    c.execute('select * from utilizador')
    row = c.fetchall()

    context = {'list_utilizador': row,'context': Utilizador.objects.filter(id_estado = 1)}
    return render(request,"list.html",context)

def fornecedor_list(request):
    from django.db import connection
    c = connection.cursor()
    c.execute('select * from fornecedor')
    row = c.fetchall()

    context = {'list_fornecedor': row,'context': Fornecedor.objects.filter(id_estado = 1)}
    return render(request,"list.html",context)