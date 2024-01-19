from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.db import connection, ProgrammingError
from django.http import JsonResponse
from psycopg2.extras import Json
from django.shortcuts import render, redirect
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
    get_user_and_sales_counts,
    venda_get_list,
    update_fornecedor,
    get_fornecedor_details,
    get_componente_details,
    update_componente,
    get_export_encomendas,
    get_venda_details,
    get_compra_details,
    get_equipamento_details,
    get_producao_details,
    get_utilizador_details,
    update_equipamento,
    ordenar_compras
)
from core.utilsMongo import (
    get_tamanho_atributo,
    get_tipo_atributo,
    get_marca_atributo,
    insert_batch_into_equipamento_comp_atrib,
)
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_protect


def masterPage(request):
    return render(request, "masterPage.html")

def import_componente_html(request):
    return render(request, "import_componente.html")

require_GET
@csrf_protect
def new_order(request):
    if 'id_utilizador' in request.session and request.session['id_utilizador'] and (request.session["nivel_acesso"] == 1 or request.session["nivel_acesso"] > 2) :
        pass
    else:
        # A variável de sessão 'id_utilizador' não existe ou não está preenchida - redireciona para login
        return redirect('/')
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
        exit
        
    result = get_user_and_sales_counts(request.session["id_utilizador"])
    result_table_venda = venda_get_list(request.session["id_utilizador"])
    result_dict = result[0]

    context = {
        "total_users": result_dict['total_users'],
        "client_users_count": result_dict['client_users_count'],
        "total_sales": result_dict['total_sales'],
        "total_orders": result_dict['total_orders'],
        "total_value_orders": result_dict['total_value_orders'],
        "low_stock_components": result_dict['low_stock_components'],
        "result_table_venda": result_table_venda,

    }

    return render(request, "dashboard.html", context)

def error404(request):
    return render(request, "404.html")

def Sem_Acesso(request):
    return render(request, "sem_acesso.html")

#####################################

def save_utilizador(request):
    if request.method == 'POST':

        # Obter os dados do formulário
        nome  = request.POST.get('nome_input')
        email = request.POST.get('email_input')
        passw = request.POST.get('password_input')

        morada     = request.POST.get('morada_input')
        localidade = request.POST.get('localidade_input')
        perfil     = request.POST.get('perfil_input')
        cliente_ch = request.POST.get('cliente_input')
        cliente    = 'TRUE' if cliente_ch else 'FALSE'  # Se marcado, cliente será 1, caso contrário, será 0
        contato    = request.POST.get('contato_input')
        cpostal    = request.POST.get('cpostal_input')

        # Executar a função no PostgreSQL
        with connection.cursor() as cursor:
            #cursor.execute("SELECT * FROM public.fn_utilizador_criar(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [nome, morada, localidade, cpostal, contato, email, passw, perfil, 1, cliente])
            #result = cursor.fetchone()
            # Montar a consulta SQL com os parâmetros
            query = "SELECT * FROM public.fn_utilizador_criar(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sql_with_values = cursor.mogrify(query, [nome, morada, localidade, cpostal, contato, email, passw, perfil, 1, cliente])  
            print("Consulta SQL:", sql_with_values)   

            # Executar a consulta
            cursor.execute(sql_with_values)
            result = cursor.fetchone()            


        ####################
        if result and result[0] > 0:  # Verifica se há um resultado e se o id_utilizador não é 0
            return HttpResponseRedirect('/utilizador/list/')
        else:
            # Se não sucedida
            return render(request, 'create_utilizador.html', {'erro': True})

    else:
        return render(request, 'create_utilizador.html')

#####################################
def new_utilizador(request):
    #html = "<html><body><h1>Criação de Novo Utilizador</h1></html>"
    #return HttpResponse(html)

     # Verifica se a variável de sessão 'id_utilizador' existe e está preenchida e nivel de acesso >1
    if 'id_utilizador' in request.session and request.session['id_utilizador'] and request.session["nivel_acesso"] > 1:
        pass
    else:
        # A variável de sessão 'id_utilizador' não existe ou não está preenchida - redireciona para login
        return redirect('/')
        
           
    resultado_marca = get_marca_atributo(request)

    context = {
        'id_atributo_marca': resultado_marca.get("id_atributo"),
        'marca_valorlista': resultado_marca.get("resultados")
    }
    return render(request, "create_utilizador.html", context)    

#####################################

def function_exists(table_name):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
    except ProgrammingError:
        return False
    return True


def generic_list(request, table_name):

    print(table_name)

    # Verifica se a variável de sessão 'id_utilizador' existe e está preenchida e nivel de acesso >1
    if 'id_utilizador' in request.session and request.session['id_utilizador'] and request.session["nivel_acesso"] > 1:
        pass
    else:
        # A variável de sessão 'id_utilizador' não existe ou não está preenchida - redireciona para login
        return redirect('/fulllogin/')
        exit
    # ----------------------------------    
    function_table_name = f"{table_name}_get_list({request.session['id_utilizador']}, 0)"
    if not function_exists(function_table_name):
        return redirect("/404")
    
    # se tabela producao
    if table_name == 'producao' :
        if request.session["nivel_acesso"] >= 3:
            pass
        else:
            return redirect('/sem_acesso/')
            exit

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
    # Verifica se a variável de sessão 'id_utilizador' existe e está preenchida e nivel de acesso >1
    if 'id_utilizador' in request.session and request.session['id_utilizador'] and request.session["nivel_acesso"] > 1:
        pass
    else:
        # A variável de sessão 'id_utilizador' não existe ou não está preenchida - redireciona para login
        return redirect('/fulllogin/')
        exit
    # ----------------------------------    

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
    if 'id_utilizador' in request.session and request.session['id_utilizador'] and request.session["nivel_acesso"] >= 4:
        pass
    else:
        return redirect('/sem_acesso/')
        exit
    if request.method == "POST":
        if table_name == "componente":
            return redirect("edit_componente", record_id=record_id)
        elif table_name == "fornecedor":
            return redirect("edit_fornecedor", record_id=record_id)
        elif table_name == "equipamento":
            return redirect("edit_equipamento", record_id=record_id)
        else:
            return redirect("generic_list", table_name=table_name)

def edit_fornecedor(request,record_id):
    if 'id_utilizador' in request.session and request.session['id_utilizador'] and request.session["nivel_acesso"] >= 4:
        pass
    else:
        return redirect('/sem_acesso/')
        exit
        
    fornecedor_details = get_fornecedor_details(record_id)

    if request.method == "POST":
        nome = request.POST.get("nome", fornecedor_details["nome"])
        endereco = request.POST.get("endereco", fornecedor_details["endereco"])
        codpostal = request.POST.get("codpostal", fornecedor_details["codigopostal"])
        localidade = request.POST.get("localidade", fornecedor_details["localidade"])
        contacto = request.POST.get("contacto", fornecedor_details["contacto"])
        email = request.POST.get("email", fornecedor_details["email"])
        id_estado = request.POST.get("id_estado", fornecedor_details["id_estado"])

        update_fornecedor(record_id, nome, endereco, codpostal, localidade, contacto, email,id_estado)

        return redirect("/fornecedor/list")
    
    return render(request, "edit_fornecedor.html", {"fornecedor": fornecedor_details})

def edit_componente(request, record_id):
    componente_details = get_componente_details(record_id)
       
    if request.method == "POST":
        descricao = request.POST.get("descricao")
        preco = request.POST.get("preco")
        pcusto_medio = request.POST.get("pcusto_medio")
        imagem = request.POST.get("imagem")
        id_estado = request.POST.get("id_estado")
        
        update_componente(record_id, descricao, preco, pcusto_medio, imagem, id_estado)

        return redirect("/componente/list")

    return render(request, "edit_componente.html", {"componente": componente_details})

def edit_equipamento(request, record_id):
    equipamento_details = get_equipamento_details(request.session['id_utilizador'], record_id)
    componente_details = equipamento_details.pop('componentes', [])
    
    if request.method == "POST":
        nome = request.POST.get("nome")
        preco = request.POST.get("preco")
        imagem = request.POST.get("imagem")
        id_estado = request.POST.get("id_estado")
        
        update_equipamento(record_id, nome, preco, imagem, id_estado)

        return redirect("/equipamento/list")

    return render(request, "edit_equipamento.html", {"equipamento": equipamento_details})


@require_POST
@csrf_protect
def detalhes_fornecedor(request, fornecedor_id):
    fornecedor_details = get_fornecedor_details(fornecedor_id)
    return JsonResponse(fornecedor_details)

@require_POST
@csrf_protect
def detalhes_componente(request, componente_id):
    componente_details = get_componente_details(componente_id)
    return JsonResponse(componente_details)

@require_POST
@csrf_protect
def detalhes_venda(request, venda_id):
    venda_details = get_venda_details(request.session["id_utilizador"], venda_id)

    equipamentos_details = venda_details.pop('equipamentos', [])

    return JsonResponse({
        'venda_details': venda_details,
        'equipamentos_details': equipamentos_details
    })

@require_POST
@csrf_protect
def detalhes_compra(request, compra_id):
    compra_details = get_compra_details(request.session["id_utilizador"], compra_id)

    componentes_details = compra_details.pop('componentes', [])

    return JsonResponse({
        'compra_details': compra_details,
        'componentes_details': componentes_details
    })

@require_POST
@csrf_protect
def detalhes_equipamento(request, equipamento_id):
    equipamento_details = get_equipamento_details(request.session["id_utilizador"], equipamento_id)

    componentes_details = equipamento_details.pop('componentes', [])

    return JsonResponse({
        'equipamento_details': equipamento_details,
        'componentes_details': componentes_details
    })

@require_POST
@csrf_protect
def detalhes_producao(request, producao_id):
    producao_details = get_producao_details(request.session["id_utilizador"], producao_id)

    componentes_details = producao_details.pop('componentes', [])

    return JsonResponse({
        'producao_details': producao_details,
        'componentes_details': componentes_details
    })

@require_POST
@csrf_protect
def detalhes_utilizador(request, utilizador_id):
    utilizador_details = get_utilizador_details(request.session["id_utilizador"], utilizador_id)
    return JsonResponse(utilizador_details)


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

    return HttpResponse(resultados)
        
def form_create_componente(request):

    # Verifica se a variável de sessão 'id_utilizador' existe e está preenchida e nivel de acesso >1
    if 'id_utilizador' in request.session and request.session['id_utilizador'] and request.session["nivel_acesso"] > 1:
        pass
    else:
        # A variável de sessão 'id_utilizador' não existe ou não está preenchida - redireciona para login
        return redirect('/fulllogin/')
        exit
    # --------------------------
            
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


def fn_populate_equipamento_comp_atrib(request, id_equipamento):    
    result = get_for_equipamento_comp_atrib(request.session["id_utilizador"], id_equipamento)
        
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
    return JsonResponse({'result': result})


def import_componente_json(request):
    if request.method == 'POST':
        json_data = request.POST.get('json', '')
        
        resultado = inserir_componentes_atributos(json_data)
            
        if(resultado == None):
            return HttpResponse("Json contém erros!")
        
        return HttpResponse(resultado) 
    
def export_encomendas(request):
    fornecedores = get_all_fornecedores(request.session["id_utilizador"], 0)
    return render(
        request,
        "export_encomendas.html",
        {"fornecedores": fornecedores},
    )

def imprimir_export_encomendas(request):

    if request.method == "POST":
        tipo = json.loads(request.POST.get("tipo"))
        if tipo == 0:#all encomendas
            resultado = get_export_encomendas(request.session["id_utilizador"], tipo, 0)
        elif tipo == 1:# all encomendas from fornecedor
            resultado = get_export_encomendas(request.session["id_utilizador"], tipo, json.loads(request.POST.get("id_fornecedor")))
        elif tipo == 2:# get specific encomenda
            resultado = get_export_encomendas(request.session["id_utilizador"], tipo, json.loads(request.POST.get("id_encomenda")))
        else:
           return HttpResponse("Método não permitido.")
        
        json_data = json.dumps(resultado, indent=2)
        return JsonResponse({'result': "success", 'json_data': json_data})
    else:
        return HttpResponse("Método não permitido.")
    
