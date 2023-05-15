from tables import db, WasteMovement, Waste, WasteType, Address, Country, Container, ContainerType, ProducerXMovement, Producer
from WasteMovementQuery import createConnection
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
import json
from datetime import date

import time
import threading

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


# Obtener los colectores de un pais usando ORM
def getWastesQuantity (quantity):

    engine = createConnection(False)
    Session = sessionmaker(bind=engine)
    session = Session()

    query = select(WasteMovement.posttime, WasteMovement.quantity, Container.containerName, Waste.wasteName, WasteType.typeName, Producer.producerName, Country.countryName).select_from(WasteMovement).join(Waste).join(WasteType).join(Address).join(Country).join(Container).join(ContainerType).join(ProducerXMovement).join(Producer).where(WasteMovement.quantity > quantity).order_by(WasteMovement.quantity.desc())
    
    result = session.execute(query)

    resultDict = []
    resultInfo = {}

    for idx, res in enumerate(result):
        resultInfo[idx] = {"posttime": res[0], "quantity": res[1], "containerName": res[2], "wasteName": res[3], "typeName": res[4], "producerName": res[5], "countryName": res[6]}
        resultDict.append(resultInfo[idx])

    jsonResult = json.dumps(resultInfo, cls=CustomEncoder)

    with open('results.json', 'w') as f:
        f.write(jsonResult)
    session.close()
    return resultDict

def run_orm(quantity, threadsAmount):
    total_time = 0
    for i in range(threadsAmount):
        start_time = time.time()
        t = threading.Thread(target=getWastesQuantity, args=(quantity,))
        t.start()
        t.join()
        end_time = time.time()
        execution_time = end_time - start_time
        total_time += execution_time
        print(f"Execution time: {execution_time*1000:.2f} milliseconds")
    return total_time