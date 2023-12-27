import pymongo

def connection(request, collection):
    myclient = pymongo.MongoClient(
        "mongodb://sysadmin:AcessoMONGO2023%24@144.91.103.133:37017/"
    )
    mydb = myclient["BDTech"]
    mycol = mydb[collection]

    return mycol


def get_all_atributos(request):
    myquery = {
        "id_equipamento": 1
    }  ## caso se queira ir buscar o que tem id_equipamento = 1
    mycol = connection(request, "equipamento_comp_atrib")
    mydoc = mycol.find()#mycol.find(myquery)

    for x in mydoc:
        print("\nmongooos", x)
        return x
    
    
def get_tipo_atributo(request, texto):
    mycol = connection(request, "atributo")
    query = {"descricao": {"$regex": f"tipo.*{texto}", "$options": "i"}}

    documentos_encontrados = mycol.find(query)
    
    resultados_formatados = []

    valor_index = 0

    for doc in documentos_encontrados:
        id_atributo = doc.get("id_atributo")
        for valor_index, valor in enumerate(doc.get("valorlista", [])):
            resultados_formatados.append({"value": str(valor_index), "text": valor})
    
    return {"resultados": resultados_formatados, "id_atributo": id_atributo}

def get_tamanho_atributo(request, texto):
    mycol = connection(request, "atributo")
    query = {"descricao": {"$regex": f"tamanho.*{texto}", "$options": "i"}}

    documentos_encontrados = mycol.find(query)
    
    resultados_formatados = []

    valor_index = 0

    for doc in documentos_encontrados:
        id_atributo = doc.get("id_atributo")
        for valor_index, valor in enumerate(doc.get("valorlista", [])):
            resultados_formatados.append({"value": str(valor_index), "text": valor})
    
    return {"resultados": resultados_formatados, "id_atributo": id_atributo}

def get_marca_atributo(request):
    mycol = connection(request, "atributo")
    query = {"descricao": {"$regex": "marca", "$options": "i"}}

    marcas_encontrados = mycol.find(query)
    resultados_formatados = {}

    for doc in marcas_encontrados:
        for valor_index, valor in enumerate(doc.get("valorlista", [])):
            resultados_formatados[str(valor_index)] = valor
    
    return {"resultados": resultados_formatados, "id_atributo": doc.get("id_atributo")}

def get_atributo_mongo_id(request, id_atributo):
    mycol = connection(request, "atributo")
    atributo = mycol.find_one({"id_atributo": id_atributo}, {"_id": 1})

    if atributo:
        return atributo["_id"]
    else:
        return None

def insert_batch_into_equipamento_comp_atrib(request, data):
    mycol = connection(request, "equipamento_comp_atrib")

    # Percorra a lista de tuplas e insira cada tupla como um documento
    for tupla in data:
        id_equipamento, id_componente, id_atributo, valoratrib = tupla

        # Obtenha o _id correspondente ao id_atributo da tabela atributo
        id_atributo_mongo = get_atributo_mongo_id(request, id_atributo)

        if id_atributo_mongo is not None:
            # Crie um documento com os valores da tupla e o _id obtido
            document_to_insert = {
                "id_equipamento": id_equipamento,
                "id_componente": id_componente,
                "id_atributo": id_atributo,
                "id_atributo_mongo": id_atributo_mongo,
                "valoratrib": valoratrib,
            }

            # Insira o documento na coleção
            result = mycol.insert_one(document_to_insert)

            # Verifique se a inserção foi bem-sucedida
            if not result.inserted_id:
                return "Erro durante a inserção."

    return "Inserção bem-sucedida!"