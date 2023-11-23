from django.http import HttpResponse
from django.template import loader

def members(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())

def dashboard(request):
  template = loader.get_template('dashboard.html')
  return HttpResponse(template.render())

def masterPage(request):
  template = loader.get_template('masterPage.html')
  return HttpResponse(template.render())