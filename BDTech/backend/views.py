from django.http import HttpResponse, HttpResponseNotFound
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
    function_table_name = f"{table_name}_get(1,0)"
    if not function_exists(function_table_name):
        return redirect('404/')

    with connection.cursor() as c:
        query = f"SELECT * FROM {function_table_name}"
        c.execute(query)
        rows = c.fetchall()
        columns = [desc[0] for desc in c.description]

    context = {"table_data": rows, "columns": columns, "table_name": table_name}
    return render(request, "list.html", context)





# def utilizador_list(request):
#     from django.db import connection

#     c = connection.cursor()
#     c.execute("select * from utilizador_get(1,0)")
#     row = c.fetchall()

#     context = {"list_utilizador": row, "context": Utilizador.objects.all}
#     return render(request, "list.html", context)