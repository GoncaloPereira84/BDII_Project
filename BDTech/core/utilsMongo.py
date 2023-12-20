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
