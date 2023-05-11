# How to use the application
- Install all dependencies with 'npm i'
- use 'npm run start' to start the app
- Using postman, send requests to check the status
    - http://localhost:5000/api/kind/saludos (GET)
    - http://localhost:5000/api/kind/saludosTo (POST) => { "quien" : "bases I" } (BODY)

## Test Procedure
CREATE PROCEDURE [dbo].[getFilteredProducers]
   @filter VARCHAR(50)
AS
BEGIN
   SELECT *
   FROM producers
   WHERE producerName LIKE '%' + @filter + '%'
END

