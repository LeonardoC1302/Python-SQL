import pyodbc
import tkinter as tk

# FUNCTIONS
def connect():
    server = 'localhost'
    database = 'caso3'
    cnxn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION=yes;')

    return cnxn

def executeQuery(cnxn, query, params):
    cursor = cnxn.cursor()
    try:
        if params == []:
            cursor.execute(query)
            connection.commit()
            return
        else:
            cursor.execute(query, params)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def createGUI(data, title):
    table_frame = tk.Frame(root)
    table_frame.pack(side="top", fill="both", expand=True)

    # create title label
    tk.Label(table_frame, text=title, font=('Helvetica', 16, 'bold'), bg="#eaeaea").grid(row=0, column=0, columnspan=len(data[0]), padx=5, pady=5)

    # create headings
    headings = ["ID", "Name", "Balance", "Percentage"]
    for i, heading in enumerate(headings):
        tk.Label(table_frame, text=heading, font=('Helvetica', 12, 'bold'), bg="#D3D3D3", borderwidth=1, relief="solid").grid(row=1, column=i, padx=5, pady=5, sticky="nsew")

    # create data rows
    for row, data_item in enumerate(data, start=2):
        data_item = list(data_item)
        data_item[2] = f"${data_item[2]:,.2f}"  # format balance as currency
        data_item[3] = f"{data_item[3]:,.2f}%"  # format percentage as percentage
        for col, value in enumerate(data_item):
            tk.Label(table_frame, text=value, font=('Helvetica', 12), borderwidth=1, relief="flat").grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    # configure row and column weights to make the table expandable
    for i in range(len(headings)):
        table_frame.columnconfigure(i, weight=1)
    for i in range(len(data) + 2):
        table_frame.rowconfigure(i, weight=1)

    return table_frame




def dataToGUI(titles):
    # tables = []
    for query in queries:
        data = executeQuery(connection, query, [contract])
        createGUI(data, titles[queries.index(query)])
        # table.pack(side="left")

# MAIN
connection = connect()
queries = [
    """
    SELECT participants.participantId, participants.participantName, participants.balance, contractParticipants.participantPercentage FROM participants
    INNER JOIN contractParticipants ON participants.participantId = contractParticipants.participantId
    WHERE contractParticipants.contractId = ?;
    """,
    """
    SELECT collectors.collectorId, collectors.collectorName, collectors.balance, contractCollectors.collectorPercentage from collectors
    INNER JOIN contractCollectors ON collectors.collectorId = contractCollectors.collectorId
    WHERE contractCollectors.contractId = ?;
    """,
    """
    SELECT producers.producerId, producers.producerName, producers.balance, contractProducers.producerPercentage FROM producers
    INNER JOIN contractProducers ON producers.producerId = contractProducers.producerId
    WHERE contractProducers.contractId = ?;
    """
]
# Create Tkinter Window
root = tk.Tk()
root.title("Contract Participants")

# Create a containers for the GUI
# main_frame = tk.Frame(root)
# main_frame.pack(side="top", fill="both", expand=True)

# tables_frame = tk.Frame(main_frame)
# tables_frame.pack(side="bottom", fill="both", expand=True)


# Execute Queries
titles = ["Participants", "Collectors", "Producers"]
contract = 1;
dataToGUI(titles)

procedure = """
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND OBJECT_ID = OBJECT_ID('dbo.registerSales'))
BEGIN
    EXEC('
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
    ');
END;
"""
execProc = """
    exec registerSales @client =1,
        @product =1,
        @seller =1,
        @totalPrice = 1000,
        @paymentType = 1,
        @contract =1;
"""
data = executeQuery(connection, procedure, [])
data = executeQuery(connection, execProc, [])

dataToGUI(titles)

connection.close()
root.mainloop()