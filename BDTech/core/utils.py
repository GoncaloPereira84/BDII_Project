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

def get_equipamentos_by_id(id_equipamento,tipo):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM get_equipamentos_by_ids(%s,%s);
            """,
            [id_equipamento,tipo],
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

    if result and result[0] and result[0][0]:
        json_result = json.loads(result[0][0])
        return json_result
    else:
        return None

def get_equipamento_by_name(nome, tipo_equipamento):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM get_equipamento_by_name(%s,%s);
            """,
            [nome, tipo_equipamento],
        )
        result = cursor.fetchall()

    if result:
        json_result = json.loads(result[0][0])
        return json_result
    else:
        return None

def obter_compras_usuario(id_utilizador):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM obter_compras_usuario(%s);
            """,
            [id_utilizador]
        )
        result = cursor.fetchall()

    return result

def detalhes_equipamentos_venda(id_venda):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM detalhes_equipamentos_venda(%s);
            """,
            [id_venda],
        )
        result = cursor.fetchall()
        
        return result


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

def venda_get_list(id_utilizador):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM venda_get_list(%s,0);
            """,
            [id_utilizador],
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

        return resultado(result)
    
def inserir_componentes_atributos(compra_json):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM inserir_componentes_atributos(%s);
                """,
                [compra_json],
            )
            result = cursor.fetchone()

            return result
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None

def criar_venda(id_utilizador, json_data):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM criar_venda(%s,%s);
                """,
                [id_utilizador, json_data],
            )
            result = cursor.fetchone()

            return result
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None

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

def atualizar_encomenda_tpdoc(id_utilizador, id_compra):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM atualizar_encomenda_tpdoc(%s, %s);
            """,
            [id_utilizador, id_compra],
        )
        result = cursor.fetchone()

    return result[0]


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

def get_user_and_sales_counts(id_utilizador):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM get_user_and_sales_counts(%s);
            """,
            [id_utilizador],
        )
        result = cursor.fetchone()
    return result

def carrinho_get_info(id_utilizador):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM carrinho_get_info(%s);
            """,
            [id_utilizador],
        )
        result = cursor.fetchall()
    return result


def check_stock_carrinho(json_data):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM check_stock_carrinho(%s);
            """,
            [json_data],
        )
        result = cursor.fetchall()
    return result

def get_export_encomendas(id_utilizador, tipo, id_funcionalidade):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM get_export_encomendas(%s,%s,%s);
            """,
            [id_utilizador, tipo, id_funcionalidade],
        )
        result = cursor.fetchone()
    return result


def obter_maximo_preco_por_tipo(tipo_id):
    with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM obter_maximo_preco_por_tipo(%s);
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

def filtrar_equipamentos_por_preco(id_equipamento, min_price, max_price):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM filtrar_equipamentos_por_preco(%s, %s::money, %s::money);
            """,
            [id_equipamento, min_price, max_price],
        )
        result = cursor.fetchall()
    print(result)

    return result

def get_equipamentos_by_preco(min_price, max_price, tipo):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM get_equipamentos_by_preco(%s::money, %s::money,%s);
            """,
            [min_price, max_price, tipo],
        )
        result = cursor.fetchall()
    print(result)
    return result

###########################
## UPDATES ##
###########################

def update_fornecedor(id,nome,endereco,codpostal,localidade,contacto,email,idestado):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM update_fornecedor(%s,%s,%s,%s,%s,%s,%s,%s)
            """, 
            [id,nome,endereco,codpostal,localidade,contacto,email,idestado]
        )
        result = cursor.fetchall()
    print(result)
    return result

def get_fornecedor_details(fornecedor_id):
    with connection.cursor() as cursor:
        cursor.execute(
             """
            SELECT get_fornecedor_details(%s) AS fornecedor_details
            """, 
            [fornecedor_id]
        )
        result = cursor.fetchone()
        
        json_result = result[0]
        details_dict = json.loads(json_result)
    return details_dict