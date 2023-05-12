# How to use the application
- Install all dependencies with 'npm i'
- use 'npm run start' to start the app
- Using postman, send requests to check the status
    - http://localhost:5000/api/kind/saludos (GET)
    - http://localhost:5000/api/kind/saludosTo (POST) => { "quien" : "bases I" } (BODY)

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

