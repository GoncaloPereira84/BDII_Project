from django.http import HttpResponse, Http404
from django.db import connection, ProgrammingError
from django.http import JsonResponse
from psycopg2.extras import Json
from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Componente,
)
from django.utils import timezone
import json

from core.utils import (
    fn_compra_inserir,
    fn_compra_componente_inserir,
    fn_get_max_ndoc_by_tpdoc,
    get_all_fornecedores,
    get_all_componente,
    get_all_tipomaoobra,
    get_all_tipoequipamento,
    fn_tipomaoobra_inserir,
    fn_componente_inserir,
    fn_inserir_componente_atributos,
    fn_equipamento_inserir,
    fn_producao_inserir,
    get_all_equipamentos,
    fn_producao_equip_existente_inserir,
    fn_check_stock_producao,
    get_for_equipamento_comp_atrib,
    atualizar_encomenda_tpdoc,
    inserir_componentes_atributos,
)
from core.utilsMongo import (
    get_tamanho_atributo,
    get_tipo_atributo,
    get_marca_atributo,
    insert_batch_into_equipamento_comp_atrib,
)


def masterPage(request):
    return render(request, "masterPage.html")

def import_componente_html(request):
    return render(request, "import_componente.html")


def new_order(request):
    fornecedores = get_all_fornecedores(request.session["id_utilizador"], 0)
    componentes = get_all_componente(request.session["id_utilizador"], 0)
    return render(
        request,
        "new_order.html",
        {"fornecedores": fornecedores, "componentes": componentes},
    )
 

def new_prod(request):
    componentes = get_all_componente(request.session["id_utilizador"], 0)
    tiposmaoobra = get_all_tipomaoobra(request.session["id_utilizador"], 0)
    tiposequipamentos = get_all_tipoequipamento(request.session["id_utilizador"], 0)
    return render(
        request,
        "prod_equip.html",
        {
            "componentes": componentes,
            "tiposmaoobra": tiposmaoobra,
            "tiposequipamentos": tiposequipamentos,
        },
    )

def new_prod_existente(request):
    equipamentos = get_all_equipamentos(request.session["id_utilizador"], 0)
    tiposmaoobra = get_all_tipomaoobra(request.session["id_utilizador"], 0)
    tiposequipamentos = get_all_tipoequipamento(request.session["id_utilizador"], 0)
    return render(
        request,
        "prod_equip_existente.html",
        {
            "equipamentos": equipamentos,
            "tiposmaoobra": tiposmaoobra,
            "tiposequipamentos": tiposequipamentos,
        },
    )


def dashboard(request):

    # Verifica se a variável de sessão 'id_utilizador' existe e está preenchida e nivel de acesso >1
    if 'id_utilizador' in request.session and request.session['id_utilizador'] and request.session["nivel_acesso"] > 1:
        pass
    else:
        # A variável de sessão 'id_utilizador' não existe ou não está preenchida - redireciona para login
        return redirect('/fulllogin/')
    # --------------------------

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_user_and_sales_counts();")
        result = cursor.fetchone()

    total_users, client_users_count, total_sales, total_orders = result

    context = {
        "total_users": total_users,
        "client_users_count": client_users_count,
        "total_sales": total_sales,
        "total_orders": total_orders,
    }

    return render(request, "dashboard.html", context)


def error404(request):
    return render(request, "404.html")

def new_utilizador(request):
    html = "<html><body><h1>Criação de Novo Utilizador</h1></html>"
    return HttpResponse(html)


def function_exists(table_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
    except ProgrammingError:
        return False
    return True


def generic_list(request, table_name):
    function_table_name = f"{table_name}_get_list(1,0)"
    if not function_exists(function_table_name):
        return redirect("/404")

    with connection.cursor() as c:
        query = f"SELECT * FROM {function_table_name}"
        c.execute(query)
        rows = c.fetchall()
        columns = [desc[0] for desc in c.description]

    rows_as_dicts = [dict(zip(columns, row)) for row in rows]

    for row in rows_as_dicts:
        row["id_field"] = row[f"n_{table_name}"]

    imagem_column_present = "imagem" in columns
    row_id = 0 if not imagem_column_present else 1

    context = {
        "table_data": rows,
        "columns": columns,
        "table_name": table_name,
        "imagem_column_present": imagem_column_present,
        "row_id": row_id,
    }
    

    return render(request, "list.html", context)


def delete_record(request, table_name, record_id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc("delete_record", [table_name, record_id])

            results = cursor.fetchone()

            if results[0] == 1:
                return redirect("/" + table_name + "/list")
            else:
                raise Http404(results[1])

    except Exception as e:
        raise Http404(str(e))


def edit_record(request, table_name, record_id):
    if request.method == "POST":
        if table_name == "componente":
            return redirect("edit_componente", record_id=record_id)
        else:
            return redirect("generic_list", table_name=table_name)


def edit_componente(request, record_id):
    componente = get_object_or_404(Componente, id_componente=record_id)

    if request.method == "POST":
        nova_descricao = request.POST.get("descricao")

        componente.descricao = nova_descricao
        componente.save()

        return redirect("/componente/list")

    return render(request, "edit_componente.html", {"componente": componente})


def save_encomenda(request):
    if request.method == "POST":
        id_fornecedor = request.POST.get("id_fornecedor")
        total_encomenda = float(request.POST.get("total_encomenda"))
        componentes_json = request.POST.get("componentes", "[]")

        componentes = json.loads(componentes_json)

        next_ndoc = fn_get_max_ndoc_by_tpdoc(request.session["id_utilizador"], "ENF")
        next_ndoc += 1

        compra_json = {
            "id_fornecedor": id_fornecedor,
            "data": timezone.now(),
            "id_estado": 1,
            "tpdoc": "ENF",
            "ndoc": next_ndoc,
            "valortotal": total_encomenda,
            "ligaid": 0,
        }

        resultado_compra = fn_compra_inserir(
            request.session["id_utilizador"], compra_json
        )
        if "id_novo" in resultado_compra:
            id_compra = resultado_compra["id_novo"]
        else:
            print("Erro a obter o id_compra")

        for componente in componentes:
            id_componente = componente["id_componente"]
            quantidade = componente["quantidade"]
            preco_unit = componente["preco_unit"]

            compra_componente_json = {
                "id_compra": id_compra,
                "id_componente": id_componente,
                "quantidade": quantidade,
                "preco_unitario": preco_unit,
            }

            fn_compra_componente_inserir(
                request.session["id_utilizador"], compra_componente_json
            )
        return HttpResponse("Compra efetuada com sucesso!")
    else:
        return HttpResponse("Método não permitido.")
    

def criar_mao_obra(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        custo_hora = float(request.POST.get("custo_hora"))

        compra_json = {
            "nome": nome,
            "custo_hora": custo_hora,
        }

        resultado = fn_tipomaoobra_inserir(
            request.session["id_utilizador"], compra_json
        )
        if "id_novo" in resultado:
            id_tipomaoobra = resultado["id_novo"]
            return JsonResponse({"message": "Tipo de mão de obra criada com sucesso!", "id_tipomaoobra": id_tipomaoobra, "nome": nome})
        else:
            return JsonResponse({"error": "Erro a obter o id_compra"})

    else:
        return JsonResponse({"error": "Método não permitido."})
    
def mango(request):
    texto_procurado = "Disco"
    resultados = get_tamanho_atributo(request, texto_procurado)
    
    valores_encontrados = resultados.get("resultados")
    id_atributo = resultados.get("id_atributo")

    # Imprime os valores encontrados
    print("Valores encontrados:")
    print(valores_encontrados)

    # Imprime os id_atributo
    print("ID Atributo Array:")
    print(id_atributo)

    return HttpResponse(resultados)
        
def form_create_componente(request):
    resultado_marca = get_marca_atributo(request)

    context = {
        'id_atributo_marca': resultado_marca.get("id_atributo"),
        'marca_valorlista': resultado_marca.get("resultados")
    }
    return render(request, "create_componente.html", context)

def get_atributo_options(request):
    tpcomponente_value = request.GET.get('tpcomponente', None)
    resultado_tipo = get_tipo_atributo(request, tpcomponente_value)
    resultado_tamanho = get_tamanho_atributo(request, tpcomponente_value)

    if resultado_tipo and resultado_tamanho:
        
        id_atributo_tipo = resultado_tipo.get("id_atributo")
        tipo_valorlista_options = resultado_tipo.get("resultados")
        
        id_atributo_tamanho = resultado_tamanho.get("id_atributo")
        tamanho_valorlista_options = resultado_tamanho.get("resultados")
        
        print(id_atributo_tipo)
        print(tipo_valorlista_options)
        print(id_atributo_tamanho)
        print(tamanho_valorlista_options)
        
        return JsonResponse({
            'id_atributo_tipo': id_atributo_tipo,
            'tipo_valorlista_options': tipo_valorlista_options,
            'id_atributo_tamanho': id_atributo_tamanho,
            'tamanho_valorlista_options': tamanho_valorlista_options,
        })
    else:
        return JsonResponse({
            'id_atributo_tipo': None,
            'tipo_valorlista_options': [],
            'id_atributo_tamanho': None,
            'tamanho_valorlista_options': [],
        })


def create_componente(request):
    if request.method == "POST":
        id_atributo_tipo= request.POST.get("id_atributo_tipo")
        tipo_valorlista_options= request.POST.get("tipo_valorlista_options")
        id_atributo_tamanho= request.POST.get("id_atributo_tamanho")
        tamanho_valorlista_options= request.POST.get("tamanho_valorlista_options")
        descricao = request.POST.get("descricao")
        preco = request.POST.get("preco")
        id_atributo_marca=  request.POST.get("id_atributo_marca")
        marca_valorlista =request.POST.get("marca_valorlista")

        componente_json = {
            "id_estado": 1,
            "descricao": descricao,
            "preco": preco,
            "quantidade_stock": 0,
            "imagem": "",
            "pcusto_medio": preco
        }

        resultado = fn_componente_inserir(
            request.session["id_utilizador"], componente_json
        )
        if "id_novo" in resultado:
            id_componente = resultado["id_novo"]
            json_atributo_data = [
                {"id_atributo": id_atributo_tipo[0], "valoratrib": tipo_valorlista_options},
                {"id_atributo": id_atributo_tamanho[0], "valoratrib": tamanho_valorlista_options},
                {"id_atributo": id_atributo_marca[0], "valoratrib": marca_valorlista},
            ]
            json_array = Json(json_atributo_data)

            resultado2 = fn_inserir_componente_atributos(
                request.session["id_utilizador"], id_componente, json_array
            )
            return HttpResponse("Componente criado")
        else:
            return JsonResponse({"error": "Erro a obter o id_componente"})
    else:
        return HttpResponse("Método não permitido.")
    

def create_equipamento(request):
    if request.method == "POST":
        componentes_json = json.loads(request.POST.get("componentes", "[]"))

        equipamento_json = {
            "id_tipoequipamento": request.POST.get("id_tipoequipamento"),
            "id_estado": 1,
            "id_moeda": 1,
            "descricao": request.POST.get("descricao"),
            "quantidade_stock": 0,
            "preco": request.POST.get("preco"),
            "imagem": request.POST.get("imagem"),
            "nome": request.POST.get("nome"),
        }

        resultado_equipamento = fn_equipamento_inserir(
            request.session["id_utilizador"], equipamento_json, Json(componentes_json) 
        )
        if "id_novo" in resultado_equipamento and resultado_equipamento["id_novo"] != 0:
            id_equipamento = resultado_equipamento["id_novo"]
            create_producao(request, id_equipamento)
            return HttpResponse("Equipamento criado")
        else:
            return HttpResponse(0)
    else:
        return HttpResponse("Método não permitido.")
    
def create_producao(request, id_equipamento):
    producao_json = {
        "id_equipamento": id_equipamento,
        "id_tipomaoobra": request.POST.get("id_tipomaoobra"),
        "id_estado": 1,
        "id_moeda": 1,
        "data": timezone.now(),
        "quantidade": request.POST.get("quantdEquip"),
        "custounitario": request.POST.get("custounitario"),
        "nhoras": request.POST.get("nhoras")
    }

    resultado_producao = fn_producao_inserir(
        request.session["id_utilizador"], producao_json 
    )
    if "id_novo" in resultado_producao:
        id_producao = resultado_producao["id_novo"]
        fn_populate_equipamento_comp_atrib(request, id_equipamento)
    else:
        print("Erro a obter o id_producao")

def create_producao_equip_existente(request):
    if request.method == "POST":
        equipamentos_json = json.loads(request.POST.get("equipamentos", "[]"))
        producao_json = {
            "id_estado": 1,
            "id_moeda": 1,
            "data": timezone.now(),
            'id_tipomaoobra': request.POST.get("id_tipomaoobra"),
            'nhoras': request.POST.get("nhoras"),
        }
        resultado_stock = fn_check_stock_producao(
            Json(equipamentos_json) 
        )
        if resultado_stock == 0:
            return HttpResponse(0)
        resultado_equipamento = fn_producao_equip_existente_inserir(
            request.session["id_utilizador"], producao_json, Json(equipamentos_json) 
        )

        if "id_novo" in resultado_equipamento and resultado_equipamento["id_novo"] != 0:
            return HttpResponse("Produção criada")
        else:
            return HttpResponse(0)
    else:
        return HttpResponse("Método não permitido.")


def fn_populate_equipamento_comp_atrib(request):    
    result = get_for_equipamento_comp_atrib(request.session["id_utilizador"], 62)
    
    print("result:",result)
    
    resultado = insert_batch_into_equipamento_comp_atrib(request, result)
    
    
def list_compra_FR_doc(request):    
    with connection.cursor() as c:
        query = "SELECT * FROM compra_fr_get_list(1)"
        c.execute(query)
        rows = c.fetchall()
        columns = [desc[0] for desc in c.description]

    rows_as_dicts = [dict(zip(columns, row)) for row in rows]

    for row in rows_as_dicts:
        row["id_field"] = row["n_compra"]

    imagem_column_present = "imagem" in columns
    row_id = 0 if not imagem_column_present else 1

    context = {
        "table_data": rows,
        "columns": columns,
        "table_name": "Encomendas recebidas",
        "imagem_column_present": imagem_column_present,
        "row_id": row_id,
    }

    return render(request, "list.html", context)

def receber_encomenda(request,record_id):    
    result = atualizar_encomenda_tpdoc(request.session["id_utilizador"], record_id)
    
    print("result:",result)
    if result == 1:
        return redirect("/compra/list/fr")
    
    
    return redirect("/compra/list/fr")

def import_componente_json(request):
    if request.method == 'POST':
        json_data = request.POST.get('json', '')
        
        resultado = inserir_componentes_atributos(json_data)
        
        return HttpResponse(resultado) 