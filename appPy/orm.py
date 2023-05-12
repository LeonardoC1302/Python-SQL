import time
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, create_engine
from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from geoalchemy2 import Geography

# create engine and session
engine = create_engine("mssql+pyodbc://localhost\SQLEXPRESS/caso3?driver=ODBC+Driver+17+for+SQL+Server")
Session = sessionmaker(bind=engine)
# session = Session()

# create base class
Base = declarative_base()

# define models for the result set
class WasteMovement(Base):
    __tablename__ = 'wasteMovements'
    wasteMovementId = Column(Integer, primary_key=True)
    posttime = Column(Date, nullable=False)
    responsibleName = Column(String(50), nullable=False)
    signImage = Column(LargeBinary, nullable=False)
    addressId = Column(Integer, ForeignKey('addresses.addressId'), nullable=False)
    movementTypeId = Column(Integer, nullable=False)
    contractId = Column(Integer, nullable=False)
    quantity = Column(Float(precision=2), nullable=False)
    userId = Column(Integer, nullable=False)
    checksum = Column(LargeBinary, nullable=False)
    computer = Column(String(50), nullable=False)
    containerId = Column(Integer, ForeignKey('containers.containerId'), nullable=False)
    wasteId = Column(Integer, ForeignKey('wastes.wasteId'), nullable=False)
    carId = Column(Integer)
    address = relationship("Address")
    container = relationship("Container")
    waste = relationship("Waste")

class Waste(Base):
    __tablename__ = 'wastes'
    wasteId = Column(Integer, primary_key=True)
    wasteType = Column(Integer, nullable=False)
    wasteName = Column(String(50), nullable=False)

class WasteType(Base):
    __tablename__ = 'wasteTypes'
    wasteTypeId = Column(Integer, primary_key=True)
    typeName = Column(String(50), nullable=False)
    recyclable = Column(LargeBinary, nullable=False)

class Address(Base):
    __tablename__ = 'addresses'
    addressId = Column(Integer, primary_key=True)
    countryId = Column(Integer, ForeignKey('countries.countryId'), nullable=False)
    stateId = Column(Integer, nullable=False)
    cityId = Column(Integer, nullable=False)
    geoLocation = Column(Geography, nullable=False)
    country = relationship("Country")

class Country(Base):
    __tablename__ = 'countries'
    countryId = Column(Integer, primary_key=True)
    countryName = Column(String(50), nullable=False)

class Container(Base):
    __tablename__ = 'containers'
    containerId = Column(Integer, primary_key=True)
    containerName = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    containerTypeId = Column(Integer, ForeignKey('containerTypes.containerTypeId'), nullable=False)
    containerType = relationship("ContainerType")

class ContainerType(Base):
    __tablename__ = 'containerTypes'
    containerTypeId = Column(Integer, primary_key=True)
    typeName = Column(String(50), nullable=False)
    brandId = Column(Integer, nullable=False)
    modelId = Column(Integer, nullable=False)
    capacity = Column(Float(precision=2), nullable=False)
    measureId = Column(Integer, nullable=False)

class ProducerXMovement(Base):
    __tablename__ = 'producersXmovements'
    producerXmovement = Column(Integer, primary_key=True)
    producerId = Column(Integer, ForeignKey('producers.producerId'), nullable=False)
    wasteMovementId = Column(Integer, ForeignKey('wasteMovements.wasteMovementId'), nullable=False)

class Producer(Base):
    __tablename__ = 'producers'
    producerId = Column(Integer, primary_key=True)
    producerName = Column(String(50), nullable=False)
    grade = Column(Float(precision=2))
    balance = Column(Float(precision=2), nullable=False)
# define the function to execute the query with the ORM
# def get_filtered_producers_orm(quantity):
#     results = session.query(WasteMovement.posttime, WasteMovement.quantity, Container.containerName,
#                             Waste.wasteName, WasteType.typeName, Producer.producerName,
#                             Country.countryName).\
#         join(Waste, Waste.wasteId == WasteMovement.wasteId).\
#         join(WasteType, WasteType.wasteTypeId == Waste.wasteType).\
#         join(Address, Address.addressId == WasteMovement.addressId).\
#         join(Country, Country.countryId == Address.countryId).\
#         join(Container, Container.containerId == WasteMovement.containerId).\
#         join(ContainerType, ContainerType.containerTypeId == Container.containerTypeId).\
#         join(ProducerXMovement, ProducerXMovement.wasteMovementId == WasteMovement.wasteMovementId).\
#         join(Producer, Producer.producerId == ProducerXMovement.producerId).\
#         filter(WasteMovement.quantity > quantity).\
#         order_by(WasteMovement.quantity.desc()).\
#         all()
#     return results



## TEST ##
# start_time = time.time()
# producers = get_filtered_producers_orm(192)
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Execution time: {execution_time} seconds")

Base.metadata.create_all(engine)
# print the results
# for producer in producers:
#     print(f"Producer ID: {producer.producerId}, Producer Name: {producer.producerName}, Grade: {producer.grade}, Balance: {producer.balance}")