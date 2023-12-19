import json
from django.db import connection
import datetime
from django.db import connection

#################
##    lists    ##
#################
def get_all_fornecedores(id_utilizador, id_fornecedor):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM fornecedor_get_list(%s, %s);
            """,
            [id_utilizador, id_fornecedor],
        )
        result = cursor.fetchall()

    return result

def get_all_equipamentos(id_utilizador, id_equipamento):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM equipamento_get_list(%s, %s);
            """,
            [id_utilizador, id_equipamento],
        )
        result = cursor.fetchall()

    return result

def get_detalhes_equipamento(id_equipamento):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM detalhes_equipamento_get(%s);
            """,
            [id_equipamento],
        )
        result = cursor.fetchall()

    if result:
        json_result = json.loads(result[0][0])

        return json_result
    else:
        return None
    
def get_top_x_equipamento(top):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM get_top_x_equipamento(%s);
            """,
            [top],
        )
        result = cursor.fetchall()

    if result:
        json_result = json.loads(result[0][0])

        return json_result
    else:
        return None
    
def get_equipamento_by_type(id_tipoequipamento):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM get_equipamento_by_type(%s);
            """,
            [id_tipoequipamento],
        )
        result = cursor.fetchall()

    if result:
        json_result = json.loads(result[0][0])

        return json_result
    else:
        return None

def get_all_componente(id_utilizador, id_componente):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM componente_get_list(%s, %s);
            """,
            [id_utilizador, id_componente],
        )
        result = cursor.fetchall()

    return result

def get_all_tipomaoobra(id_utilizador, id_tipomaoobra):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM tipo_maoobra_get_list(%s, %s);
            """,
            [id_utilizador, id_tipomaoobra],
        )
        result = cursor.fetchall()

    return result

def get_all_tipoequipamento(id_utilizador, id_tipoequipamento):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM tipo_equipamento_get_list(%s, %s);
            """,
            [id_utilizador, id_tipoequipamento],
        )
        result = cursor.fetchall()

    return result

#################
##   inserts   ##
#################
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

def fn_tipomaoobra_inserir(id_utilizador, tipomaoobra_json):
    tipomaoobra_json_str = json.dumps(tipomaoobra_json)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM fn_tipomaoobra_inserir(%s, %s);
            """,
            [id_utilizador, tipomaoobra_json_str],
        )
        result = cursor.fetchone()

        return resultado(result)

#################
##   updates   ##
#################
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

#################
## single gets ##
#################
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
