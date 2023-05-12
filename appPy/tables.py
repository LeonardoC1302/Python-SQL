"mssql+pyodbc://localhost\SQLEXPRESS/caso3?driver=ODBC+Driver+17+for+SQL+Server"
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, LargeBinary
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geography

# Declaracion de las tablas como objetos para el ORM y realizar las consultas
db = SQLAlchemy()

class WasteMovement(db.Model):
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

class Waste(db.Model):
    __tablename__ = 'wastes'
    wasteId = Column(Integer, primary_key=True)
    wasteType = Column(Integer, ForeignKey('wasteTypes.wasteTypeId'), nullable=False)
    wasteName = Column(String(50), nullable=False)

class WasteType(db.Model):
    __tablename__ = 'wasteTypes'
    wasteTypeId = Column(Integer, primary_key=True)
    typeName = Column(String(50), nullable=False)
    recyclable = Column(LargeBinary, nullable=False)

class Address(db.Model):
    __tablename__ = 'addresses'
    addressId = Column(Integer, primary_key=True)
    countryId = Column(Integer, ForeignKey('countries.countryId'), nullable=False)
    stateId = Column(Integer, nullable=False)
    cityId = Column(Integer, nullable=False)
    geoLocation = Column(Geography, nullable=False)

class Country(db.Model):
    __tablename__ = 'countries'
    countryId = Column(Integer, primary_key=True)
    countryName = Column(String(50), nullable=False)

class Container(db.Model):
    __tablename__ = 'containers'
    containerId = Column(Integer, primary_key=True)
    containerName = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    containerTypeId = Column(Integer, ForeignKey('containerTypes.containerTypeId'), nullable=False)

class ContainerType(db.Model):
    __tablename__ = 'containerTypes'
    containerTypeId = Column(Integer, primary_key=True)
    typeName = Column(String(50), nullable=False)
    brandId = Column(Integer, nullable=False)
    modelId = Column(Integer, nullable=False)
    capacity = Column(Float(precision=2), nullable=False)
    measureId = Column(Integer, nullable=False)

class ProducerXMovement(db.Model):
    __tablename__ = 'producersXmovements'
    producerXmovement = Column(Integer, primary_key=True)
    producerId = Column(Integer, ForeignKey('producers.producerId'), nullable=False)
    wasteMovementId = Column(Integer, ForeignKey('wasteMovements.wasteMovementId'), nullable=False)

class Producer(db.Model):
    __tablename__ = 'producers'
    producerId = Column(Integer, primary_key=True)
    producerName = Column(String(50), nullable=False)
    grade = Column(Float(precision=2))
    balance = Column(Float(precision=2), nullable=False)
