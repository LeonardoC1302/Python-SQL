from tables import db, WasteMovement, Waste, WasteType, Address, Country, Container, ContainerType, ProducerXMovement, Producer
from WasteMovementQuery import createConnection
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

# Obtener los colectores de un pais usando ORM
def getWastesQuantity (quantity):

    engine = createConnection(False)
    Session = sessionmaker(bind=engine)
    session = Session()

    # query = select(Collector.name).select_from(Collector).join(Office).join(Address).join(Country).where(Country.name == quantity)
    query = select(WasteMovement.posttime, WasteMovement.quantity, Container.containerName, Waste.wasteName, WasteType.typeName, Producer.producerName, Country.countryName).select_from(WasteMovement).join(Waste).join(WasteType).join(Address).join(Country).join(Container).join(ContainerType).join(ProducerXMovement).join(Producer).where(WasteMovement.quantity > quantity).order_by(WasteMovement.quantity.desc())
    
    result = session.execute(query)

    # Crear lista vacia
    resultDict = []

    # Recorrer el resultado y agregarlo a la lista como diccionario para JSON
    for res in result:
        # Se crea el diccionario con el nombre. 
        # "name" es el nombre de la columna en la tabla y res[0] el valor
        resultDict.append({"name": res[0]})

    return resultDict

# print("Query executed successfully")
getWastesQuantity(900)