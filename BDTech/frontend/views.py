from django.http import HttpResponse, HttpResponseNotFound
from django.db import connection, ProgrammingError
from django.template import loader
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.


def masterPageFront(request):
    return render(request, "masterPageFront.html")

def index(request):
    return render(request, "index.html")


def kanban(request):
    return render(request, "kanban.html")  


# @csrf_exempt
# def login_utilizador(request):
#     if request.method == "POST":
#         email = request.POST.get("login-username")
#         password = request.POST.get("login-password")

#         print(f"Email: {email}, Password: {password}")

#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM login_utilizador(%s, %s);", [email, password])
#             result = cursor.fetchone()

#         if result:
#             id_utilizador, nome, email = result
#             # print(
#             #     f"User {email} logged in successfully. User ID: {id_utilizador}, Name: {nome}"
#             # )

#             # Armazenar informações na sessão
#             request.session["id_utilizador"] = id_utilizador
#             request.session["nome"] = nome
#             request.session["email"] = email

#             # Imprimir o conteúdo da sessão
#             # print(f"Session Data: {request.session.items()}")

#             messages.success(request, "Login successful.")
#             return redirect("/index")

#         else:
#             #print("Invalid credentials. Please try again.")
#             messages.error(request, "Invalid credentials. Please try again.")
#             return redirect("/index")

#     return HttpResponse("Invalid request method.")



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

