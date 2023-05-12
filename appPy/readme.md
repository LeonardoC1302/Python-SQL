# TASKS
- The solutions architect needs you to design the way in which the programs will interact with the database, defining the necessary layers to access and work with it from the applications

- To do this, you will have to try two forms of interconnectivity, the first, make a client-server access from an application programmed in the language of your choice, for example .net, java, go, python, etc., one that allows you to build a UI and that exists a native driver, jdbc, ado.net and ultimately odbc. Choose one of the following screens to carry out your test program: a) check the waste that a collector transporter is going to take from a waste producer, exchanging the respective containers b) record the sales of recycled products by assigning respective amounts according to contracts (validate the mockup of the selected screen with the design of the database and the teacher)

- The second way must be done through a REST api, for this the teacher will provide you with a base made in nodejs , to test it, implement a stored procedure that returns at least 500 records, then proceed to enable two endpoints that call Said stored procedure, respecting the layers of the REST service provided, one must make use of a connection pool and another that does not use it. Endpoints should return json.

- Once the above is done, proceed to test your rest service with postman, doing stress tests without exceeding 20 threads of execution and determine in the metrics of postman versus the metrics of the activity monitor of your sql server, which of the endpoints obtains better performance and the why, this can be documented between postman, a document, screenshots and any other supporting material

- The review of this preliminary will be with a review appointment with the assistant, the application and the rest service must be in a single git repository, the commits of each member will be taken into account

- 15 extra points will be given if you implement and measure another endpoint using an ORM

- The last commit in git should be on May 11 at midnight

# Requirements
- pip install customtkinter
- pip install sqlalchemy pyodbc
- pip install geoalchemy2
- pip install pymysql
- pip install flask
- pip install flask_sqlalchemy

# Stored Procedure
CREATE PROCEDURE GetWasteMovementsByQuantity
    @quantity INT
AS
BEGIN
    SELECT dbo.wasteMovements.posttime, dbo.wasteMovements.quantity, dbo.containers.containerName, dbo.wastes.wasteName, dbo.wasteTypes.typeName, dbo.producers.producerName, dbo.countries.countryName
    FROM dbo.wasteMovements 
    INNER JOIN dbo.wastes ON dbo.wasteMovements.wasteId = dbo.wastes.wasteId 
    INNER JOIN dbo.wasteTypes ON dbo.wastes.wasteType = dbo.wasteTypes.wasteTypeId 
    INNER JOIN dbo.addresses ON dbo.wasteMovements.addressId = dbo.addresses.addressId 
    INNER JOIN dbo.countries ON dbo.addresses.countryId = dbo.countries.countryId 
    INNER JOIN dbo.containers ON dbo.wasteMovements.containerId = dbo.containers.containerId 
    INNER JOIN dbo.containerTypes ON dbo.containers.containerTypeId = dbo.containerTypes.containerTypeId 
    INNER JOIN dbo.producersXmovements ON dbo.wasteMovements.wasteMovementId = dbo.producersXmovements.wasteMovementId 
    INNER JOIN dbo.producers ON dbo.producersXmovements.producerId = dbo.producers.producerId
    WHERE quantity > @quantity ORDER BY quantity DESC;
END

- EXEC GetWasteMovementsByQuantity @quantity = 992