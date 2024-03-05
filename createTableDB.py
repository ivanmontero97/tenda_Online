from clientPS import *


category="""CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
    );"""
subcategory="""
CREATE TABLE subcategory (
	subcategory_id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	category_id INT NOT NULL,
	created_at TIMESTAMP,
	updated_at TIMESTAMP,
	FOREIGN KEY (category_id) REFERENCES category(category_id)
);
"""
product="""
CREATE TABLE product (
	product_id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	description TEXT,
	company VARCHAR(255) NOT NULL,
	price DECIMAL(10,2) NOT NULL,
	units NUMERIC,
	subcategory_id INT NOT NULL,
	created_at TIMESTAMP,
	updated_at TIMESTAMP,
	FOREIGN KEY (subcategory_id) REFERENCES subcategory(subcategory_id)
);
"""


def createTables(query:str):
    try:
        conn=db_client()
        cur=conn.cursor()
        cur.execute(query)
        conn.commit() #Hacemos un commit de los cambios en la BD
    except Exception as e:
        conn.rollback() #Hacemos rollback en caso de no se ejecute correctamente
        print("Ha habido un error " , e)
    finally:
        cur.close()

#Las llamadas a createTable para crear las tablas , las comentamos una vez las hemos creado.
# createTables(category)
# createTables(subcategory)
# createTables(product)