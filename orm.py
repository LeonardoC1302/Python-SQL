from sqlalchemy import create_engine, Column, Integer, String, Float, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import time

# create engine and session
engine = create_engine("mssql+pyodbc://localhost\SQLEXPRESS/caso3?driver=ODBC+Driver+17+for+SQL+Server")
Session = sessionmaker(bind=engine)
session = Session()

# create model for the producers table
Base = declarative_base()

class Producer(Base):
    __tablename__ = 'producers'
    producerId = Column(Integer, primary_key=True)
    producerName = Column(String(50), nullable=False)
    grade = Column(Float(5, 2))
    balance = Column(Float(18, 2), nullable=False)

# execute stored procedure and return results as a list of Producer objects
def get_filtered_producers(filter):
    results = session.execute(text(f"EXEC getFilteredProducers @filter='{filter}'"))
    producers = []
    for row in results:
        producer = Producer(
            producerId=row.producerId,
            producerName=row.producerName,
            grade=row.grade,
            balance=row.balance
        )
        producers.append(producer)
    return producers


## TEST ##
start_time = time.time()
producers = get_filtered_producers('john')
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")


# print the results
for producer in producers:
    print(f"Producer ID: {producer.producerId}, Producer Name: {producer.producerName}, Grade: {producer.grade}, Balance: {producer.balance}")
