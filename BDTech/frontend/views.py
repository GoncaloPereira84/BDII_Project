from django.http import HttpResponse, HttpResponseNotFound
from django.db import connection, ProgrammingError
from django.template import loader
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

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



@csrf_exempt
def login_utilizador(request):
    if request.method == 'POST':
        # Get the values from the form submission
        email = request.POST.get('login-email')  # Adjust the field name if needed
        password = request.POST.get('login-password')  # Adjust the field name if needed

        # Print values to the console for debugging
        print(f'Email: {email}, Password: {password}')

        # Call PostgreSQL function
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM login_utilizador(%s, %s);", ["admin@admin.com", password])
            result = cursor.fetchone()

        if result:
            # User exists, perform further actions if needed
            id_utilizador, nome, email = result
            print(f'User {email} logged in successfully. User ID: {id_utilizador}, Name: {nome}')
            return HttpResponse(f'User {email} logged in successfully. User ID: {id_utilizador}, Name: {nome}')
        else:
            # User does not exist or password is incorrect
            print('Invalid credentials. Please try again.')
            return HttpResponse('Invalid credentials. Please try again.')

    # Handle other HTTP methods if needed
    return HttpResponse('Invalid request method.')



