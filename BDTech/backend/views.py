from django.http import HttpResponse, Http404
from django.db import connection, ProgrammingError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    Componente,
    Fornecedor,
    TipoMaoObra,
    TipoEquipamento,
)
from django.utils import timezone
import json
from .utils import (
    fn_compra_inserir,
    fn_compra_componente_inserir,
    fn_update_stock_componente,
    fn_get_max_ndoc_by_tpdoc,
    get_all_fornecedores,
    get_all_componente,
    get_all_tipomaoobra,
    get_all_tipoequipamento,
    fn_tipomaoobra_inserir,
)


def masterPage(request):
    return render(request, "masterPage.html")


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


def dashboard(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_user_and_sales_counts();")
        result = cursor.fetchone()

    total_users, client_users_count, total_sales = result

    context = {
        "total_users": total_users,
        "client_users_count": client_users_count,
        "total_sales": total_sales,
    }

    return render(request, "dashboard.html", context)


def error404(request):
    return render(request, "404.html")


def function_exists(table_name):
    print(table_name)
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
    except ProgrammingError:
        return False
    return True


def generic_list(request, table_name):
    print(table_name)
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
    print("imagem:", imagem_column_present)
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
    print(record_id)
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

            fn_update_stock_componente(
                request.session["id_utilizador"], id_componente, quantidade
            )

        return HttpResponse("Encomenda criada com sucesso!")
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
        else:
            print("Erro a obter o id_compra")

        return HttpResponse("Tipo de mão de obra criada com sucesso!")
    else:
        return HttpResponse("Método não permitido.")
    
