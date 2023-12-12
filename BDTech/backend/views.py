from django.http import HttpResponse, HttpResponseNotFound, Http404 
from django.db import connection, ProgrammingError
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from .models import Componente, Fornecedor


def masterPage(request):
    return render(request, "masterPage.html")

def new_order(request):
    fornecedores = Fornecedor.objects.all()
    componentes = Componente.objects.all()
    return render(request, "new_order.html", {"fornecedores": fornecedores, "componentes": componentes})


def dashboard(request):
    # Chama a função SQL usando o cursor do Django
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_user_and_sales_counts();")
        result = cursor.fetchone()

    # Obtém os resultados da função
    total_users, client_users_count, total_sales = result

    # Passa os resultados para o template
    context = {
        'total_users': total_users,
        'client_users_count': client_users_count,
        'total_sales': total_sales,
    }

    return render(request, "dashboard.html", context)

def error404(request):
    return render(request, "404.html")

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
        return redirect('/404') 

    with connection.cursor() as c:
        query = f"SELECT * FROM {function_table_name}"
        c.execute(query)
        rows = c.fetchall()
        columns = [desc[0] for desc in c.description]
        
    rows_as_dicts = [dict(zip(columns, row)) for row in rows]

    for row in rows_as_dicts:
        row['id_field'] = row[f"n_{table_name}"]

    imagem_column_present = 'imagem' in columns
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
    try:
        with connection.cursor() as cursor:
            cursor.callproc('delete_record', [table_name, record_id])

            results = cursor.fetchone()

            if results[0] == 1:
                return redirect('/'+table_name+'/list') 
            else:
                raise Http404(results[1])

    except Exception as e:
        raise Http404(str(e))

def edit_record(request, table_name, record_id):
    if request.method == 'POST':

        if table_name == 'componente':
            return redirect('edit_componente', record_id=record_id)
        else:
            return redirect('generic_list', table_name=table_name)


def edit_componente(request, record_id):
    componente = get_object_or_404(Componente, id_componente=record_id)

    if request.method == 'POST':
        nova_descricao = request.POST.get('descricao')

        componente.descricao = nova_descricao
        componente.save()

        return redirect('/componente/list') 

    return render(request, 'edit_componente.html', {'componente': componente})
