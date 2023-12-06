from django.http import HttpResponse, HttpResponseNotFound, Http404 
from django.db import connection, ProgrammingError
from django.template import loader
from django.shortcuts import render, redirect

def masterPage(request):
    template = loader.get_template("masterPage.html")
    return HttpResponse(template.render())


def dashboard(request):
    template = loader.get_template("dashboard.html")
    return HttpResponse(template.render())

def error404(request):
    template = loader.get_template("404.html")
    return HttpResponse(template.render())

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
    
    context = {"table_data": rows, "columns": columns, "table_name": table_name}
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

    return render(request, 'delete_record.html', {'table_name': table_name, 'record_id': record_id})
