-- SQLBook: Code
-- Registrar las ventas de productos reciclados realizando la asignación de montos respectivos según contratos
-- SQLBook: Code
CREATE PROCEDURE [dbo].[registerSales] 
    @client INT,
    @product INT,
    @seller INT,
    @totalPrice DECIMAL(12,2),
    @paymentType INT,
    @contract INT
AS
BEGIN 

    DECLARE @sellerPercentage decimal(5,2);
    DECLARE @producerPercentage decimal(5,2);
    DECLARE @collectorPercentage decimal(5,2);
    
    INSERT INTO [dbo].[sales]([clientId], [productId], [sellerId], [totalPrice], [posttime], [checksum], [paymentTypeId], [contractId]) VALUES
        (@client, @product, @seller, @totalPrice, GETDATE(), NULL, @paymentType, @contract);
        

    SET @sellerPercentage = (SELECT participantPercentage FROM contractParticipants
        INNER JOIN contracts ON contractParticipants.contractId = contracts.contractId
        WHERE contractParticipants.contractId = @contract AND 
            contractParticipants.participantId = @seller);

    -- Update seller's balance
    UPDATE participants
		SET participants.balance = participants.balance + @totalPrice * (@sellerPercentage/100)
		where participants.participantId = @seller;
    -- Update producers balance
    UPDATE producers
        SET producers.balance = producers.balance + @totalPrice * (contractProducers.producerPercentage / 100)
        FROM contracts
        INNER JOIN contractProducers ON contracts.contractId = contractProducers.contractId
        INNER JOIN producers ON contractProducers.producerId = producers.producerId
        WHERE contracts.contractId = @contract;
    -- Update collectors balance
    UPDATE collectors
        SET collectors.balance = collectors.balance + @totalPrice * (contractCollectors.collectorPercentage / 100)
        FROM contracts
        INNER JOIN contractCollectors ON contracts.contractId = contractCollectors.contractId
        INNER JOIN collectors ON contractCollectors.collectorId = collectors.collectorId
        WHERE contracts.contractId = @contract;
END;
-- SQLBook: Code
IF NOT EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND OBJECT_ID = OBJECT_ID('dbo.registerSales'))
BEGIN
    CREATE PROCEDURE [dbo].[registerSales] 
        @client INT,
        @product INT,
        @seller INT,
        @totalPrice DECIMAL(12,2),
        @paymentType INT,
        @contract INT
    AS
    BEGIN 

        DECLARE @sellerPercentage decimal(5,2);
        DECLARE @producerPercentage decimal(5,2);
        DECLARE @collectorPercentage decimal(5,2);

        INSERT INTO [dbo].[sales]([clientId], [productId], [sellerId], [totalPrice], [posttime], [checksum], [paymentTypeId], [contractId]) VALUES
            (@client, @product, @seller, @totalPrice, GETDATE(), NULL, @paymentType, @contract);


        SET @sellerPercentage = (SELECT participantPercentage FROM contractParticipants
            INNER JOIN contracts ON contractParticipants.contractId = contracts.contractId
            WHERE contractParticipants.contractId = @contract AND 
                contractParticipants.participantId = @seller);

        -- Update seller''s balance
        UPDATE participants
            SET participants.balance = participants.balance + @totalPrice * (@sellerPercentage/100)
            where participants.participantId = @seller;
        -- Update producers balance
        UPDATE producers
            SET producers.balance = producers.balance + @totalPrice * (contractProducers.producerPercentage / 100)
            FROM contracts
            INNER JOIN contractProducers ON contracts.contractId = contractProducers.contractId
            INNER JOIN producers ON contractProducers.producerId = producers.producerId
            WHERE contracts.contractId = @contract;
        -- Update collectors balance
        UPDATE collectors
            SET collectors.balance = collectors.balance + @totalPrice * (contractCollectors.collectorPercentage / 100)
            FROM contracts
            INNER JOIN contractCollectors ON contracts.contractId = contractCollectors.contractId
            INNER JOIN collectors ON contractCollectors.collectorId = collectors.collectorId
            WHERE contracts.contractId = @contract;
    END;
END;
-- SQLBook: Code
exec registerSales @client =1,
    @product =1,
    @seller =1,
    @totalPrice = 1000,
    @paymentType = 1,
    @contract =1;
-- SQLBook: Code
SELECT * FROM participants
INNER JOIN contractParticipants ON participants.participantId = contractParticipants.participantId
WHERE contractParticipants.contractId = ?;

-- SQLBook: Code
SELECT * from collectors
INNER JOIN contractCollectors ON collectors.collectorId = contractCollectors.collectorId
WHERE contractCollectors.contractId = ?;
-- SQLBook: Code
SELECT * FROM producers
INNER JOIN contractProducers ON producers.producerId = contractProducers.producerId
WHERE contractProducers.contractId = ?;