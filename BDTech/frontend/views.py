from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from .models import Utilizador
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from core.utils import (
    get_detalhes_equipamento,
    get_equipamento_by_type,
    get_top_x_equipamento,
    get_equipamento_by_name,
    obter_compras_usuario,
    detalhes_equipamentos_venda
)

def masterPageFront(request):
    return render(request, "masterPageFront.html")

def index(request):
    ultimos_equipamentos = get_top_x_equipamento(6)
    marcas = [
        {'nome': 'Apple', 'logo_url': 'https://th.bing.com/th/id/R.24e62b73004a5fb7a7a5d9c26963ed07?rik=nzIAxmu0duWlgA&riu=http%3a%2f%2fwww.zdnet.de%2fwp-content%2fuploads%2f2013%2f05%2fapple-logo-schwarz.jpg&ehk=q59%2b69Oq6FABvF0DbfJTGBD7m4IqvKMyNFPSzy8pRRg%3d&risl=&pid=ImgRaw&r=0'},
        {'nome': 'Lenovo', 'logo_url': 'https://th.bing.com/th/id/OIP.IRDIAwBmlFyff6g1EuFjXwHaEZ?rs=1&pid=ImgDetMain'},
        {'nome': 'Asus', 'logo_url': 'https://th.bing.com/th/id/OIP.M78UplVnuECVc6nFgq8p1wHaFj?w=640&h=480&rs=1&pid=ImgDetMain'},
        {'nome': 'MSI', 'logo_url': 'https://th.bing.com/th/id/OIP.S9Dvja4R5tcjaPYe381o0gHaEK?rs=1&pid=ImgDetMain'},
    ]
    return render(request, 'index.html', {'equipamentos': ultimos_equipamentos, 'marcas': marcas})

def kanban(request):
    return render(request, "filtro.html")  

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




def equipamento_type(request, tipo):
    if tipo:
        equipamentos = get_equipamento_by_type(tipo)
    return render(request, 'filtro.html', {'equipamentos': equipamentos})
   

def detalhes_equipamento(request, equipamento_id):
    equipamento = get_detalhes_equipamento(equipamento_id)
    return render(request, 'detalhes_equipamento.html', {'equipamento': equipamento[0]})
    


def pesquisa_equipamento(request):
    termo_pesquisa = request.GET.get('dm-booking-destination', '')
    categoria = request.GET.get('categoria', '')
   
    if categoria :
        id_categoria = int(categoria)
    else: 
        id_categoria = 0
    
    # Obter equipamentos com base no termo de pesquisa e categoria
    equipamentos = get_equipamento_by_name(termo_pesquisa, id_categoria)

    # Se houver um único resultado, redirecione para a página de detalhes
    if len(equipamentos) == 1:
        equipamento_id = equipamentos[0]['id_equipamento']
        return redirect('detalhes_equipamento', equipamento_id)

    # Se houver mais de um resultado ou nenhum, exiba uma página de resultados de pesquisa
    return render(request, 'filtro.html', {'equipamentos': equipamentos, 'termo_pesquisa': termo_pesquisa, 'categoria': id_categoria})



def usercompras(request):
    
    utilizador = request.session["id_utilizador"]
    vendas = obter_compras_usuario(utilizador)
    resultado = [{'nome_utilizador': row[0],
                'id_venda': row[1],
                'data_venda': row[2],
                'valortotal': row[3],
                'tpdoc': row[4],
                'ndoc': row[5]} for row in vendas]
    return render(request, 'usercompras.html', {'vendas': resultado})

def detalhes_venda(request, venda_id):
    utilizador = request.session.get("id_utilizador")

    if utilizador is not None:
        detalhes = detalhes_equipamentos_venda(venda_id)
        resultado = [
            {
                'id_venda': row[0],
                'nome': row[1],
                'quantidade': row[2],
                'valortotal': row[3],
                'data_venda': row[4],
                'precounitario': row[5]
            }
            for row in detalhes
        ]

        # Agrupar resultados pelo id_venda
        detalhes_agrupados = {}
        for row in resultado:
            id_venda = row['id_venda']
            if id_venda not in detalhes_agrupados:
                detalhes_agrupados[id_venda] = {
                    'id_venda': id_venda,
                    'data_venda': row['data_venda'],
                    'valortotal': row['valortotal'],
                    'itens': []
                }
            detalhes_agrupados[id_venda]['itens'].append({
                'nome': row['nome'],
                'quantidade': row['quantidade'],
                'precounitario': row['precounitario']
            })

        return render(request, 'detalhes_venda.html', {'detalhes': detalhes_agrupados.values()})

    else:
        return HttpResponseBadRequest("ID do utilizador não encontrado na sessão.")
