from clientPS import *
from producteSchema import *
from csvService import *


def getAllProducts():
    try:
        clientDB = db_client() #Abrimos un cliente , que establece la conexión con la base de datos
        cur = clientDB.cursor()#Abrimos un cursor para hacer consultas y querys a la BD
        cur.execute("Select * from product") #Ejecutamos la consulta
        result = cur.fetchall()
        data = products_schema(result)
    except Exception as e:
        data = {"status":-1,"error":f'{e}'}
    finally:
        clientDB.close()
        return data
    
def getProduct(id):
    try:
        clientDB = db_client() #Abrimos un cliente , que establece la conexión con la base de datos
        cur = clientDB.cursor()#Abrimos un cursor para hacer consultas y querys a la BD
        cur.execute(f"Select * from product where product_id={id}") #Ejecutamos la consulta
        result = cur.fetchone()
        data = product_schema(result)
    except Exception as e:
        data = {"status":-1,"error":f'{e}'}
    finally:
        clientDB.close()
        return data
    
def insertProduct(product_id,name,description, company, price,units, subcategory_id):
    try:
        clientDB = db_client() #Abrimos un cliente , que establece la conexión con la base de datos
        cur = clientDB.cursor()#Abrimos un cursor para hacer consultas y querys a la BD
        cur.execute(f"""INSERT INTO product (product_id,name,description, company, price,units, subcategory_id,created_at,updated_at) 
                    VALUES({product_id},'{name}','{description}','{company}',{price},{units},{subcategory_id}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);""") #Ejecutamos la consulta
        clientDB.commit()
    except Exception as e:
        clientDB.rollback()
    finally:
        cur.close()
        clientDB.close()

def updateProduct(product_id,name,description, company, price,units, subcategory_id):
    try:
        clientDB = db_client() #Abrimos un cliente , que establece la conexión con la base de datos
        cur = clientDB.cursor()#Abrimos un cursor para hacer consultas y querys a la BD
        cur.execute(f"""update product
                    set name='{name}',description='{description}', company='{company}', price={price},units={units}, subcategory_id={subcategory_id}, created_at=CURRENT_TIMESTAMP, updated_at=CURRENT_TIMESTAMP  
                    where product_id={product_id}""") #Ejecutamos la consulta
        clientDB.commit()
    except Exception as e:
        clientDB.rollback()
    finally:
        cur.close()
        clientDB.close()
    
def deleteProduct(id:int):
    try:
        clientDB = db_client() #Abrimos un cliente , que establece la conexión con la base de datos
        cur = clientDB.cursor()#Abrimos un cursor para hacer consultas y querys a la BD
        cur.execute(f"""delete from product
                    where product_id={id}""") #Ejecutamos la consulta
        clientDB.commit()
    except Exception as e:
        print(f'Error: {e}')
        clientDB.rollback()       
    finally:
        cur.close()
        clientDB.close()

def getSomeInformationAllProducts():    
    try:
        clientDB = db_client() #Abrimos un cliente , que establece la conexión con la base de datos
        cur = clientDB.cursor()#Abrimos un cursor para hacer consultas y querys a la BD
        cur.execute(f"""Select 
                        cat.name AS category_name ,
                        sub.name AS subcategory_name,
                        prod.name AS product_name,
                        prod.company AS product_brand,
                        prod.price AS  product_price
                        FROM 
                            product prod
                        JOIN 
                            subcategory sub ON prod.subcategory_id = sub.subcategory_id
                        JOIN
                            category cat ON sub.category_id = cat.category_id""") #Ejecutamos la consulta
        result = cur.fetchall()
        data = allProducts_schema(result)
        clientDB.commit()
    except Exception as e:
        clientDB.rollback()
        data = {"status":-1,"error":f'{e}'}
    finally:
        clientDB.close()
        return data


#InsercionesMasivas desde CSV a la BD
def insertCategory():
    clientDB = db_client() #Abrimos un cliente , que establece la conexión con la base de datos
    cur = clientDB.cursor()#Abrimos un cursor para hacer consultas y querys a la BD
    try:
        listaCategory = loadCSVCategory('llista_productes.csv')
        for item in listaCategory:
            id_categoria=item['category_id']
            nombre_categoria=item['name_category']

            #Comprobación de si existe este item en la BD
            cur.execute(f"""SELECT * FROM category where category_id = {id_categoria}""")
            validationQuery = cur.fetchone()

            #Si no existe se hace un insert
            if not validationQuery:
                insert= (f"""INSERT INTO category( category_id, name, created_at, updated_at)
                    VALUES ({id_categoria}, '{nombre_categoria}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);""")   
                cur.execute(insert) 
            
            clientDB.commit()
    except Exception as e:
      clientDB.rollback()
      print('Error : ', e)    
    finally:
      cur.close()

def insertSubCategory():
    clientDB = db_client() #Abrimos un cliente , que establece la conexión con la base de datos
    cur = clientDB.cursor()#Abrimos un cursor para hacer consultas y querys a la BD
    try:
        listaSubCategory = loadCSVSubcategory('llista_productes.csv')
        for item in listaSubCategory:
            id_categoria= item['category_id']
            id_subcategoria= item['subcategory_id']
            nombre_subcategoria= item['name_subcategory']

            #Comprobación de si existe este item en la BD
            cur.execute(f"""SELECT * FROM subcategory where subcategory_id = {id_subcategoria}""")
            validationQuery = cur.fetchone()

            #Si no existe se hace un insert
            if not validationQuery:
                insert= (f"""INSERT INTO subcategory( subcategory_id, name,category_id, created_at, updated_at)
                    VALUES ({id_subcategoria}, '{nombre_subcategoria}','{id_categoria}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);""")   
                cur.execute(insert)
                clientDB.commit()
    except Exception as e:
      clientDB.rollback()
      print('Error : ', e)    
    finally:
      cur.close()

def insertProducts():
    clientDB = db_client() #Abrimos un cliente , que establece la conexión con la base de datos
    cur = clientDB.cursor()#Abrimos un cursor para hacer consultas y querys a la BD
    try:
        listaProductos = loadCSVProduct('llista_productes.csv')
        for item in listaProductos:
            id_prod= item['product_id']
            nom_prod= item['name_product']
            descripcion= item['description']
            company = item["company"]
            precio= item["price"]
            unid = item["units"]
            subcategory_id = item["subcategory_id"]
            #Comprobación de si existe este item en la BD
            cur.execute(f"""SELECT * FROM product where product_id  = {id_prod}""")
            validationQuery = cur.fetchone()

            #Si no existe se hace un insert
            if not validationQuery:
                insert= (f"""INSERT INTO product(
	                        product_id, name, description, company, price, units, subcategory_id, created_at, updated_at)
	                        VALUES ({id_prod}, '{nom_prod}', '{descripcion}', '{company}', {precio}, {unid}, {subcategory_id}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);""")
                cur.execute(insert)     
                clientDB.commit()
       
    except Exception as e:
      clientDB.rollback()
      print('Error : ', e)    
    finally:
      cur.close()

# insertCategory()
# insertSubCategory()
# insertProducts()
#deleteProduct(1005) Me funciona el servicio a mano, no me funciona 