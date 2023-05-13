from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

# Crear la conexion con el servidor de base de datos
# pool: True si se desea usar un pool de conexiones, False si no
def createConnection(pool):
    username = "root"
    password = "123456"
    # username = "frank"
    # password = "frank"
    server = "localhost"
    port = "1433"
    db = "caso3"
    driver = "ODBC Driver 17 for SQL Server"
    if pool:
        engine = create_engine(f"mssql+pyodbc://{username}:{password}@{server}:{port}/{db}?driver={driver}", pool_size=10, max_overflow=0)
    else:
        engine = create_engine(f"mssql+pyodbc://{username}:{password}@{server}:{port}/{db}?driver={driver}", poolclass=NullPool)
    return engine

# Ejecutar un query (SP) en la base de datos con parametros
def getWastesQuantity(pool, quantity):
    engine = createConnection(pool)
    param = quantity
    query = text("EXEC GetWasteMovementsByQuantity:param")
    with engine.connect() as connection:
        result = connection.execute(query, {"param": param})
        # Convertir el resultado a una lista con diccionarios
        keys = result.keys()
        resultDict = [dict(zip(keys, row)) for row in result.fetchall()]

        return resultDict