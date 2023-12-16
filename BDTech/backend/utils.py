import json
from django.db import connection
import datetime


def datetime_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def resultado(result):
    if result:
        return {"resultado": result[0], "id_novo": result[1]}
    else:
        return {"resultado": "ERRO", "id_novo": 0}


def fn_compra_inserir(id_utilizador, compra_json):
    compra_json_str = json.dumps(compra_json, default=datetime_serializer)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM fn_compra_inserir(%s, %s);
            """,
            [id_utilizador, compra_json_str],
        )
        result = cursor.fetchone()

        return resultado(result)


def fn_compra_componente_inserir(id_utilizador, compra_componente_json):
    compra_json_str = json.dumps(compra_componente_json)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM fn_compra_componente_inserir(%s, %s);
            """,
            [id_utilizador, compra_json_str],
        )
        result = cursor.fetchone()

    return resultado(result)

def fn_update_stock_componente(id_utilizador, id_componente, quantidade_stock):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM fn_update_stock_componente(%s, %s, %s);
            """,
            [id_utilizador, id_componente, quantidade_stock],
        )
        result = cursor.fetchone()

    return resultado(result)

def fn_get_max_ndoc_by_tpdoc(id_utilizador, tpdoc):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM fn_get_max_ndoc_by_tpdoc(%s, %s);
            """,
            [id_utilizador, tpdoc],
        )
        result = cursor.fetchone()

    return result[0]
