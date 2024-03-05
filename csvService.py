import pandas as pd

#Hacemos 3 funciones para cargar en cada una de ellas una lista que devolvemos con la categoria , subcategoria y productos. Que posteriormente trataremos para hacer inserts en la BD

def loadCSVCategory(file):
    #Creamos la lista donde guardaramos los datos leidos del csv
    listaCategory=[]
    #Leemos fichero
    datosCSV = pd.read_csv(file,header= 0)
    for index,row in datosCSV.iterrows():
        #para cada fila lo pasamos a un diccionario
        fila = row.to_dict()
        listaAux= getCategory(fila["id_categoria"],fila['nom_categoria'])
        listaCategory.append(listaAux)
        #Para cada entidad cogemos sus valores
    return listaCategory

def loadCSVSubcategory(file):
    #Creamos la lista donde guardaramos los datos leidos del csv
    listaSubCategory=[]
    #Leemos fichero
    datosCSV = pd.read_csv(file,header= 0)
    for index,row in datosCSV.iterrows():
        #para cada fila lo pasamos a un diccionario
        fila = row.to_dict()
        listaAux= getSubCategory(fila["id_subcategoria"],fila['id_categoria'],fila["nom_subcategoria"])
        listaSubCategory.append(listaAux)
        #Para cada entidad cogemos sus valores
    return listaSubCategory

def loadCSVProduct(file):
    #Creamos la lista donde guardaramos los datos leidos del csv
    listaProduct=[]
    #Leemos fichero
    datosCSV = pd.read_csv(file,header= 0)
    for index,row in datosCSV.iterrows():
        #para cada fila lo pasamos a un diccionario
        fila = row.to_dict()
        listaAux= getProducto(fila["id_producto"], fila['nom_producto'], fila["descripcion_producto"], 
                                          fila["companyia"],fila["precio"], fila["unidades"],fila["id_subcategoria"])
        listaProduct.append(listaAux)
        #Para cada entidad cogemos sus valores
    return listaProduct

#Funciones auxiliares para extraer de cada fila un JSON del item que meteremos en la lista.
def getCategory(category_id,name):
    return {'category_id': category_id, 'name_category': name}
def getSubCategory(subcategory_id,category_id,name):
    return {'subcategory_id':subcategory_id, 'category_id': category_id, 'name_subcategory': name}
def getProducto(product_id, name_product, description, company, price, units, subcategory_id):
    return { 'product_id': product_id, 'name_product': name_product, 'description': description, 'company':company, 'price': price, 
            'units': units, 'subcategory_id': subcategory_id}
