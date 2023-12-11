from django.http import HttpResponse, HttpResponseNotFound
from django.db import connection, ProgrammingError
from django.template import loader
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Equipamento


def masterPageFront(request):
    return render(request, "masterPageFront.html")

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
    return render(request, "kanban.html")  

@csrf_exempt
def login_utilizador(request):
    if request.method == "POST":
        email = request.POST.get("login-username")
        password = request.POST.get("login-password")

        # print(f"Email: {email}, Password: {password}")

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM login_utilizador(%s, %s);", [email, password])
            result = cursor.fetchone()

        if result:
            id_utilizador, nome, email = result
            # print(
            #     f"User {email} logged in successfully. User ID: {id_utilizador}, Name: {nome}"
            # )

            request.session["id_utilizador"] = id_utilizador
            request.session["nome"] = nome
            request.session["email"] = email

            # print(f"Session Data: {request.session.items()}")

            return JsonResponse({'success': True, 'redirect': '/'})

        else:
            # print("Invalid credentials. Please try again.")
            return JsonResponse({'success': False, 'message': 'Credenciais Inválidas'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@csrf_exempt
def logout_utilizador(request):
            try:
                del request.session["id_utilizador"]
                del request.session["nome"]
                del request.session["email"]
                return redirect("/")
            except KeyError:
                pass
            return HttpResponse("You're logged out.")

