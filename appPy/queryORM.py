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

    resultDict = []

    for res in result:

        resultDict.append({"posttime": res[0], "quantity": res[1], "containerName": res[2], "wasteName": res[3], "typeName": res[4], "producerName": res[5], "countryName": res[6]})

    return resultDict

selected = getWastesQuantity(900)
print(selected)