from django.http import HttpResponse, HttpResponseBadRequest
from django.db import connection
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from core.utils import (
    get_detalhes_equipamento,
    get_equipamento_by_type,
    get_top_x_equipamento,
    get_equipamento_by_name,
    obter_compras_usuario,
    detalhes_equipamentos_venda,
    obter_maximo_preco_por_tipo,
    get_equipamentos_by_id,
    filtrar_equipamentos_por_preco,
    get_equipamentos_by_preco,
    carrinho_get_info,
    check_stock_carrinho,
    criar_venda,
)
from core.utilsMongo import get_marcas, get_ram, get_rom, aplicar_filtros

from django.http import HttpResponseRedirect
from decimal import Decimal

import json


def masterPageFront(request):
    return render(request, "masterPageFront.html")


def index(request):
    ultimos_equipamentos = get_top_x_equipamento(6)
    marcas = [
        {
            "nome": "Apple",
            "logo_url": "https://th.bing.com/th/id/R.24e62b73004a5fb7a7a5d9c26963ed07?rik=nzIAxmu0duWlgA&riu=http%3a%2f%2fwww.zdnet.de%2fwp-content%2fuploads%2f2013%2f05%2fapple-logo-schwarz.jpg&ehk=q59%2b69Oq6FABvF0DbfJTGBD7m4IqvKMyNFPSzy8pRRg%3d&risl=&pid=ImgRaw&r=0",
        },
        {
            "nome": "Lenovo",
            "logo_url": "https://th.bing.com/th/id/OIP.IRDIAwBmlFyff6g1EuFjXwHaEZ?rs=1&pid=ImgDetMain",
        },
        {
            "nome": "Asus",
            "logo_url": "https://th.bing.com/th/id/OIP.M78UplVnuECVc6nFgq8p1wHaFj?w=640&h=480&rs=1&pid=ImgDetMain",
        },
        {
            "nome": "MSI",
            "logo_url": "https://th.bing.com/th/id/OIP.S9Dvja4R5tcjaPYe381o0gHaEK?rs=1&pid=ImgDetMain",
        },
    ]
    return render(
        request, "index.html", {"equipamentos": ultimos_equipamentos, "marcas": marcas}
    )


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

            return JsonResponse({"success": True, "redirect": "/"})

        else:
            # print("Invalid credentials. Please try again.")
            return JsonResponse({"success": False, "message": "Credenciais Inválidas"})

    return JsonResponse({"success": False, "message": "Invalid request method."})


@csrf_exempt
def logout_utilizador(request):
    try:
        del request.session["id_utilizador"]
        del request.session["nome"]
        del request.session["email"]
        del request.session["carrinho"]
        return redirect("/")
    except KeyError:
        pass
    return redirect("/")


# view login
def fulllogin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM dologin_utilizador(%s, %s)", [username, password]
            )
            result = cursor.fetchone()

        if (
            result and result[0] > 0
        ):  # Verifica se há um resultado e se o id_utilizador não é 0
            # Autenticação bem-sucedida
            # implementar a lógica de login
            id_utilizador, nome, email, id_perfil, nivel_acesso, msg = result

            request.session["id_utilizador"] = id_utilizador
            request.session["nome"] = nome
            request.session["email"] = email
            request.session["id_perfil"] = id_perfil
            request.session["nivel_acesso"] = nivel_acesso

            if id_perfil == 2:
                return HttpResponseRedirect("/dashboard/")
            else:
                return HttpResponseRedirect("/")

        else:
            return render(request, "login.html", {"erro": True})

    else:
        return render(request, "login.html")


def equipamento_type(request, tipo):
    if tipo:
        equipamentos = get_equipamento_by_type(tipo)
        nome = "Portáteis" if tipo == 1 else "Desktops"

        maxpricefiltro = obter_maximo_preco_por_tipo(tipo)

        # get marcas
        marcas = get_marcas(request)
        # get ram
        ram = get_ram(request)
        # get rom
        rom = get_rom(request)

        context = {"marcas": marcas, "ram": ram, "rom": rom}

    return render(
        request,
        "filtro.html",
        {
            "equipamentos": equipamentos,
            "nome": nome,
            "tipo_selecionado": tipo,
            "maxpricefiltro": maxpricefiltro,
            **context,
        },
    )


def detalhes_equipamento(request, equipamento_id):
    equipamento = get_detalhes_equipamento(equipamento_id)
    lista = get_top_x_equipamento(6)
    return render(request, "detalhes_equipamento.html", {"equipamento": equipamento[0], "lista": lista})


def pesquisa_equipamento(request):
    termo_pesquisa = request.GET.get("dm-booking-destination", "")
    categoria = request.GET.get("categoria", "")

    if categoria:
        id_categoria = int(categoria)
    else:
        id_categoria = 0

    # Obter equipamentos com base no termo de pesquisa e categoria
    equipamentos = get_equipamento_by_name(termo_pesquisa, id_categoria)

    # Se houver um único resultado, redirecione para a página de detalhes
    if len(equipamentos) == 1:
        equipamento_id = equipamentos[0]["id_equipamento"]
        return redirect("detalhes_equipamento", equipamento_id)

    # Se houver mais de um resultado ou nenhum, exiba uma página de resultados de pesquisa
    return render(
        request,
        "filtro.html",
        {
            "equipamentos": equipamentos,
            "termo_pesquisa": termo_pesquisa,
            "categoria": id_categoria,
        },
    )


def usercompras(request):
    utilizador = request.session["id_utilizador"]
    vendas = obter_compras_usuario(utilizador)
    resultado = [
        {
            "nome_utilizador": row[0],
            "id_venda": row[1],
            "data_venda": row[2],
            "valortotal": row[3],
            "tpdoc": row[4],
            "ndoc": row[5],
        }
        for row in vendas
    ]
    return render(request, "usercompras.html", {"vendas": resultado})


def detalhes_venda(request, venda_id):
    utilizador = request.session.get("id_utilizador")

    if utilizador is not None:
        detalhes = detalhes_equipamentos_venda(venda_id)
        resultado = [
            {
                "id_venda": row[0],
                "nome": row[1],
                "quantidade": row[2],
                "valortotal": row[3],
                "data_venda": row[4],
                "precounitario": row[5],
            }
            for row in detalhes
        ]

        # Agrupar resultados pelo id_venda
        detalhes_agrupados = {}
        for row in resultado:
            id_venda = row["id_venda"]
            if id_venda not in detalhes_agrupados:
                detalhes_agrupados[id_venda] = {
                    "id_venda": id_venda,
                    "data_venda": row["data_venda"],
                    "valortotal": row["valortotal"],
                    "itens": [],
                }
            detalhes_agrupados[id_venda]["itens"].append(
                {
                    "nome": row["nome"],
                    "quantidade": row["quantidade"],
                    "precounitario": row["precounitario"],
                }
            )

        return render(
            request, "detalhes_venda.html", {"detalhes": detalhes_agrupados.values()}
        )

    else:
        return HttpResponseBadRequest("ID do utilizador não encontrado na sessão.")


def aplicarpreco(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        precos = data.get("precos", {})
        tipo = data.get("tipo")
        min_price = precos.get("min", 0)
        max_price = precos.get("max", 1)
        min_price_decimal = Decimal(min_price)
        max_price_decimal = Decimal(max_price)

        # Formatando como uma string monetária
        min_price_str = "${:,.0f}".format(min_price_decimal)
        max_price_str = "${:,.0f}".format(max_price_decimal)

        if len(str(min_price)) <= 6:
            min_price_str = min_price_str.replace(",", ".")

        if len(str(max_price)) <= 6:
            max_price_str = max_price_str.replace(",", ".")
        print("ids_equipamento", min_price_str, max_price_str, tipo)
        ids_equipamento = get_equipamentos_by_preco(min_price_str, max_price_str, tipo)
        print("ids_equipamento", ids_equipamento)
        if ids_equipamento is not None:
            # Obter os ids como uma lista
            ids_equipamento = [item[0] for item in ids_equipamento]
        else:
            # Se ids_equipamento for None, definir como uma lista vazia
            ids_equipamento = []

        equipamentos_filtrados = get_equipamentos_by_id(ids_equipamento, tipo)
        equipamentos_dict_list = [
            {
                "id_equipamento": equipamento[1],
                "nome": equipamento[3],
                "preco": equipamento[5],
                "imagem": equipamento[0],
            }
            for equipamento in equipamentos_filtrados
        ]

        equipamentos_serializados = [
            {
                "id_equipamento": equipamento["id_equipamento"],
                "nome": equipamento["nome"],
                "preco": equipamento["preco"],
                "imagem": equipamento["imagem"],
            }
            for equipamento in equipamentos_dict_list
        ]

        return JsonResponse(
            {
                "resultados": equipamentos_serializados,
            }
        )
    else:
        return JsonResponse(
            {
                "error": "Método não permitido. Use POST para esta rota.",
            },
            status=405,
        )


def aplicarfiltros(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        marcas = data.get("marcas", [])
        precos = data.get("precos", {})
        ram = data.get("ram", [])
        rom = data.get("rom", [])
        tipo = data.get("tipo")
        print("wxem", marcas, precos, ram, rom, tipo)
        resultados = aplicar_filtros(
            request, marcas=marcas, precos=precos, ram=ram, rom=rom
        )
        print("wxem", resultados)
        if resultados:
            ids_equipamento = resultados

            equipamentos_filtrados = get_equipamentos_by_id(ids_equipamento, tipo)

            equipamentos_ids = [
                equipamento[1] for equipamento in equipamentos_filtrados
            ]

            print("equipamentos_ids", equipamentos_ids)
            min_price = precos.get("min", 0)
            max_price = precos.get("max", 1)

            min_price_decimal = Decimal(min_price)
            max_price_decimal = Decimal(max_price)

            # Formatando como uma string monetária
            min_price_str = "${:,.0f}".format(min_price_decimal)
            max_price_str = "${:,.0f}".format(max_price_decimal)

            if len(str(min_price)) <= 6:
                min_price_str = min_price_str.replace(",", ".")

            if len(str(max_price)) <= 6:
                max_price_str = max_price_str.replace(",", ".")

            if max_price_decimal >= 1000000:
                max_price_str = "${:,.0f}".format(max_price_decimal).replace(",", "")

                print("max_price_str", max_price_str)
            if len(str(max_price_decimal)) > 6:
                min_price_str = (
                    "${:,.0f}".format(min_price_decimal)
                    .replace(",", "")
                    .replace("$", "$.")
                )

            equipamentos_filtrados = filtrar_equipamentos_por_preco(
                equipamentos_ids, min_price_str, max_price_str
            )

            equipamentos_dict_list = [
                {
                    "id_equipamento": equipamento[1],
                    "nome": equipamento[3],
                    "preco": equipamento[5],
                    "imagem": equipamento[0],
                }
                for equipamento in equipamentos_filtrados
            ]

            # Continuação do seu código...
            equipamentos_serializados = [
                {
                    "id_equipamento": equipamento["id_equipamento"],
                    "nome": equipamento["nome"],
                    "preco": equipamento["preco"],
                    "imagem": equipamento["imagem"],
                }
                for equipamento in equipamentos_dict_list
            ]
            print("wxem", equipamentos_serializados)
            return JsonResponse(
                {
                    "resultados": equipamentos_serializados,
                }
            )
        else:
            return JsonResponse(
                {
                    "resultados": [],
                }
            )
    else:
        return JsonResponse(
            {
                "error": "Método não permitido. Use POST para esta rota.",
            },
            status=405,
        )


def adicionar_ao_carrinho(request):
    if request.method == "POST":
        carrinho = request.session.get("carrinho", [])

        id_equipamento = request.POST.get("id_equipamento")
        nome = request.POST.get("nome")
        imagem = request.POST.get("imagem")
        preco = request.POST.get("preco")

        equipamento_existente = None

        for equipamento in carrinho:
            if equipamento["id_equipamento"] == id_equipamento:
                equipamento_existente = equipamento
                break

        if equipamento_existente:
            equipamento_existente["quantidade"] = (
                equipamento_existente.get("quantidade", 1) + 1
            )
        else:
            equipamento = {
                "id_equipamento": id_equipamento,
                "nome": nome,
                "imagem": imagem,
                "preco": preco.replace("$", ""),
                "quantidade": 1,
            }
            carrinho.append(equipamento)

        request.session["carrinho"] = carrinho
        return JsonResponse({"carrinho": carrinho})
    else:
        return HttpResponse("Método não permitido.")


def get_carrinho_data(request):
    carrinho_data = request.session.get("carrinho", [])
    total_preco = 0.0

    for item in carrinho_data:
        preco_str = item.get("preco", "0.00").replace("$", "").replace(",", "")
        total_preco += float(preco_str) * float(item.get("quantidade"))

    carrinho_data.append({"total_preco": "{:.2f}".format(total_preco)})
    return JsonResponse(carrinho_data, safe=False)


def remover_do_carrinho(request):
    try:
        id_equipamento = request.POST.get("id_equipamento")
        carrinho = request.session.get("carrinho", [])
        carrinho = [
            item for item in carrinho if item["id_equipamento"] != id_equipamento
        ]

        request.session["carrinho"] = carrinho
        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


def mudar_quantidade_carrinho(request):
    try:
        id_equipamento = request.POST.get("id_equipamento")
        tipo = request.POST.get("tipo")
        carrinho = request.session.get("carrinho", [])

        for item in carrinho:
            if item["id_equipamento"] == id_equipamento:
                if tipo == "1":
                    item["quantidade"] += 1
                elif tipo == "0":
                    if item["quantidade"] == 1:
                        return remover_do_carrinho(request)
                    else:
                        item["quantidade"] -= 1
                break

        request.session["carrinho"] = carrinho
        request.session.save()

        return JsonResponse({"success": True, "carrinho": carrinho})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


def finalizarCarrinho(request):
    carrinho = request.session["carrinho"]
    utilizador_data_table = carrinho_get_info(request.session["id_utilizador"])

    utilizador_data = [
        {
            "nome": row[0],
            "endereco": row[1],
            "localidade": row[2],
            "codpostal": row[3],
            "contacto": row[4],
            "email": row[5],
        }
        for row in utilizador_data_table
    ]
    return render(request, "finalizarCompra.html", {"carrinhodata": carrinho, "utilizador_data": utilizador_data})

def completeCarrinho(request):
    carrinho = request.session["carrinho"]
    
    # Convert carrinho to the desired JSON format
    carrinho_json = json.dumps([{'id_equipamento': item['id_equipamento'], 'quantidade': item['quantidade']} for item in carrinho])
    
    resultado = check_stock_carrinho(carrinho_json)
    
    if resultado:
        response_data = {"error": True, "resultado": resultado}
        return JsonResponse(response_data)
    
    
    insert_result = criar_venda(request.session["id_utilizador"], json.dumps(carrinho))
    if insert_result[0] == 1:
        request.session["carrinho"] = []
        response_data = {"success": True, "resultado": resultado}
    else:
        response_data = {"errorInPostgresql": True, "resultado": "Erro no servidor"};
    return JsonResponse(response_data)

    
    
    

    
