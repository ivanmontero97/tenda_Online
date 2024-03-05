from typing import *
from fastapi import FastAPI
from productService import *
from productModel import *


app = FastAPI()



# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# # @app.get("/product/")
# # def getProduct():
# #     productDB.consulta()
# #     return{"masseage"}


#Obtener todos los productos
@app.get("/product/")
def product():
    try:
        return getAllProducts()
    except Exception as e: 
        print(f'Error: {e}')
#Consultar producto por ID
@app.get("/product/{id}")
def getProduct_Id(id:int):
    try:
        return getProduct(id) 
    except Exception as e: 
        print(f'Error: {e}')

#Añadir producto
@app.post("/product")
def insertPro(prod: Product):
    try:
        print("Received data:", prod)
        insertProduct(prod.product_id,prod.name,prod.description, prod.company, prod.price,prod.units, prod.subcategory_id)
        data = {"status":1,"Data":"Inserción realizada con éxito"}
    except Exception as e:
        data = {"status":-1,"error":f'{e}'}
    finally:
        return data


#Modificar producto
@app.put("/product/{id}")
def updateProd(id:int , prod : Product):
    try:
        updateProduct(prod.product_id,prod.name,prod.description, prod.company, prod.price,prod.units, prod.subcategory_id)
        data = {"status":1,"Data":"Modificación realizada con éxito"}
    except Exception as e:
        data = {"status":-1,"error":f'{e}'}
    finally:
        return data

#Eliminar producto
@app.delete("/product/{id}")
def deleteProd(id: int):
    try:
        deleteProduct(id) 
        data = {"status":1,"Data":"Eliminación realizada con éxito"}
    except Exception as e:
        data = {"status":-1,"error":f'{e}'}
    finally:
        return data


#Consultar categoria , subcategoria y producto
@app.get("/productAll/")
def getProductAll():
    try:
        return getSomeInformationAllProducts()
    except Exception as e: 
        print(f'Error: {e}')


#CargaMasiva de Productos
@app.post("/loadProducts/")
def insertItemsCSVToDB():
    try:
        insertCategory()
        insertSubCategory()
        insertProducts()
        data = {"status":1,"message":"Inserción masiva realizada con éxito"}
    except Exception as e: 
        data = {"status":-1,"error":f'{e}', "message":"Los datos ya existían en la BD"}
    finally:
        return data