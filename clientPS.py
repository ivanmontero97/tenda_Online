import psycopg 

def db_client():
    connexio="""
            dbname=postgres
            user=user_postgres
            password=pass_postgres
            host=localhost
            port=5432
            """
    try:
        return psycopg.connect(connexio)
    except Exception as e :
        print(f'Error conexion {e}')