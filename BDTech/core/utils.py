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
    
def fn_componente_inserir(id_utilizador, componente_json):
    componente_json_str = json.dumps(componente_json)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM fn_componente_inserir(%s, %s);
            """,
            [id_utilizador, componente_json_str],
        )
        result = cursor.fetchone()

        return resultado(result)
    
def fn_inserir_componente_atributos(id_utilizador, id_componente, componente_json):

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM inserir_componente_atributos(%s, %s, %s);
            """,
            [id_utilizador, id_componente, componente_json],
        )
        result = cursor.fetchone()

        return resultado(result)

def fn_equipamento_inserir(id_utilizador, equipamento_json, componente_json):
    equipamento_json_str = json.dumps(equipamento_json)
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM fn_equipamento_inserir(%s, %s, %s);
            """,
            [id_utilizador, equipamento_json_str, componente_json],
        )
        result = cursor.fetchone()

        return resultado(result)
    
def fn_producao_inserir(id_utilizador, equipamento_json):
    equipamento_json_str = json.dumps(equipamento_json, default=datetime_serializer)
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM fn_producao_inserir(%s, %s);
            """,
            [id_utilizador, equipamento_json_str],
        )
        result = cursor.fetchone()

        return resultado(result)
    
def fn_producao_equip_existente_inserir(id_utilizador, producao_json, equipamentos_json):
    producao_json_str = json.dumps(producao_json, default=datetime_serializer)
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM fn_producao_equip_existente_inserir(%s, %s, %s);
            """,
            [id_utilizador, producao_json_str, equipamentos_json],
        )
        result = cursor.fetchone()
        print(result)

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



def obter_maximo_preco_por_tipo(tipo_id):
    with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT obter_maximo_preco_por_tipo(%s);
                """,
                [tipo_id],
            )
            result = cursor.fetchone()
    return result[0]

def fn_check_stock_producao(equipamentos_json):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM fn_check_stock_producao(%s);
            """,
            [equipamentos_json],
        )
        result = cursor.fetchone()

    return result[0]


###########################
## equipamento_comp_atrib##
###########################
def get_for_equipamento_comp_atrib(id_utilizador, id_equipamento):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM get_for_equipamento_comp_atrib(%s, %s);
            """,
            [id_utilizador, id_equipamento],
        )
        result = cursor.fetchall()
    print(result)

    return result