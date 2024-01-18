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
        return x    

 #filtros - get marcas
def get_marcas(request):
    mycol = connection(request, "atributo")
    myquery = {"descricao": "Marca"}
    mydoc = mycol.find(myquery)

    marcas_lista = []

    for doc in mydoc:
      valores = doc.get('valorlista', [])
      for valor in valores:
        marcas_lista.append({
            "id_atributo": doc.get("id_atributo"),
            "valor": valor
        })
    return marcas_lista

#filtros - get ram
def get_ram(request):
    mycol = connection(request, "atributo")
    myquery = {"descricao": "Tamanho Ram"}
    mydoc = mycol.find(myquery)

    ram_lista = []

    for doc in mydoc:
        valores = doc.get('valorlista', [])
        for valor in valores:
            ram_lista.append({
                "id_atributo": doc.get("id_atributo"),
                "valor": valor
            })

    return ram_lista

#filtros - get rom
def get_rom(request):
    mycol = connection(request, "atributo")
    myquery = {"descricao": "Armazenamento"}
    mydoc = mycol.find(myquery)

    rom_lista = []

    for doc in mydoc:
       valores = doc.get('valorlista', [])
       for valor in valores:
            rom_lista.append({
                "id_atributo": doc.get("id_atributo"),
                "valor": valor
            })
    return rom_lista

def aplicar_filtros(request, marcas=None, precos=None, ram=None, rom=None):
    mycol = connection(request, "equipamento_comp_atrib")
    ids_equipamento = set()

    # Lista para armazenar os resultados intermediários para cada filtro
    resultados_por_filtro = []

    if marcas:
        pipeline = []
        for marca in marcas:
            pipeline.append({"$match": {"id_atributo": int(marca['id_atributo']), "valoratrib": marca['valor']}})
        pipeline.extend([
            {"$group": {"_id": "$id_equipamento"}},
            {"$project": {"_id": 0, "id_equipamento": "$_id"}}
        ])
        resultados_por_filtro.append(list(mycol.aggregate(pipeline)))

    if ram:
        pipeline = [
            {"$match": {"valoratrib": {"$in": [ram_item['valor'] for ram_item in ram]}}},
            {"$group": {"_id": "$id_equipamento"}},
            {"$project": {"_id": 0, "id_equipamento": "$_id"}}
        ]
        resultados_por_filtro.append(list(mycol.aggregate(pipeline)))

    if rom:
        pipeline = [
            {"$match": {"valoratrib": {"$in": [rom_item['valor'] for rom_item in rom]}}},
            {"$group": {"_id": "$id_equipamento"}},
            {"$project": {"_id": 0, "id_equipamento": "$_id"}}
        ]
        resultados_por_filtro.append(list(mycol.aggregate(pipeline)))

    # Realizar a interseção dos conjuntos de IDs obtidos para cada filtro
    if resultados_por_filtro:
       ids_equipamento = set(tuple(resultado.values())[0] for resultado in resultados_por_filtro[0])
       for resultados in resultados_por_filtro[1:]:
            ids_equipamento.intersection_update(tuple(resultado.values())[0] for resultado in resultados)

    return list(ids_equipamento)


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

    for tupla in data:
        id_equipamento, id_componente, id_atributo, valoratrib = tupla

        id_atributo_mongo = get_atributo_mongo_id(request, id_atributo)

        if id_atributo_mongo is not None:
            document_to_insert = {
                "id_equipamento": id_equipamento,
                "id_componente": id_componente,
                "id_atributo": id_atributo,
                "id_atributo_mongo": id_atributo_mongo,
                "valoratrib": valoratrib,
            }

            result = mycol.insert_one(document_to_insert)

            if not result.inserted_id:
                return "Erro durante a inserção."

    return "Inserção bem-sucedida!"