import pyodbc
import tkinter as tk
import tkinter.messagebox
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image as img
from typing import Union, Callable

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

# Create Custom Spinbox for Tkinter
class FloatSpinbox(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 product: tuple = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command
        self.product = product

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = ctk.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = ctk.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = ctk.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "0.0")

    def add_button_callback(self):
        # print(self.products)
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            if value >= 0:  # check that value is positive
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
                app.price = app.price + self.product[2]
                newPrice = "Total Price: ₡" + str(app.price)
                app.textPrice.set(newPrice) # Total price of products
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) - self.step_size
            if value >= 0:  # check that value is positive
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
                app.price = app.price - self.product[2]
                newPrice = "Total Price: ₡" + str(app.price)
                app.textPrice.set(newPrice) # Total price of products
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))

# Create main window of app
class App(ctk.CTk):
    def __init__(self, products):
        super().__init__()
        # Window settings
        self.title('Register Sales')
        self.geometry(f"{1100}x{580}")
        
        # create 2x2 grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, minsize=20)
        self.rowconfigure(1, weight=1)

        self.infoSection = None # Section for info
        self.price = 0 # Total price of products
        self.textPrice = tk.StringVar(value="Total Price: ₡" + str(self.price)) # Total price of products

        # Window main label (Title)
        textTitle = tk.StringVar(value="Buy Your Products")
        labelTitle = ctk.CTkLabel(self,
                                textvariable=textTitle,
                                width=10,
                                height=1,
                                fg_color="transparent",
                                font=("Arial", 30, "bold"),
                                corner_radius=8)
        labelTitle.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        # Add side image
        sideImage = ctk.CTkImage(light_image=img.open("appPy/img/darkImg.png"),
                                dark_image=img.open("appPy/img/darkImg.png"),
                                size=(200, 200))

        button = ctk.CTkButton(self, image=sideImage, text="", fg_color="transparent", bg_color="transparent", state="disabled")
        button.grid(row=1, column=0, sticky="nsew", columnspan=1, rowspan=2)

        ## Select Quantity of products
        scrollFrameQuantity = ctk.CTkScrollableFrame(self,
                            label_text="Select Your Products")
        scrollFrameQuantity.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        scrollFrameQuantity.grid_columnconfigure(0, weight=1)
        scrollFrameQuantity.grid_columnconfigure(1, weight=1)

        spinboxesP = []
        for i in range(len(products)-1):
            spinbox = FloatSpinbox(scrollFrameQuantity, width=150, step_size=1, product=products[i])
            spinboxesP.append(spinbox)
            spinbox.grid(row=i, column=1, padx=10, pady=(0, 20), sticky="w")
            spinboxLabel = ctk.CTkLabel(scrollFrameQuantity, text=products[i][1])
            spinboxLabel.grid(row=i, column=0, padx=10, pady=(0, 20), sticky="e")

        ## Price Label
        priceLabel = ctk.CTkLabel(self,
                                textvariable=self.textPrice,
                                width=10,
                                height=1,
                                fg_color="transparent",
                                font=("Arial", 30, "bold"),
                                corner_radius=8)
        priceLabel.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)
        ## Submit button
        buttonSubmit = ctk.CTkButton(self,
                                    fg_color="transparent",
                                    border_width=2,
                                    text_color=("gray10", "#DCE4EE"),
                                    corner_radius=30,
                                    text="Submit Order",
                                    # command=lambda:print(self.textPrice))
                                    command=lambda:self.placeOrder(products, spinboxesP))
        buttonSubmit.grid(row=4, column=1, sticky="nsew", padx=10, pady=10)

        ## CheckInfo button
        buttonInfo = ctk.CTkButton(self,
                                    fg_color="transparent",
                                    border_width=2,
                                    text_color=("gray10", "#DCE4EE"),
                                    corner_radius=30,
                                    text="Check Information",
                                    command=self.checkInfo)
        buttonInfo.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)
    # Place Order
    def showSummary(self, saleProducts):
        summary = "Sale Summary:\n\n"
        total_price = 0
        
        for product in saleProducts:
            product_name = str(product[0])
            product_price = str(product[1])
            available = product[2]
            
            if available:
                summary += f"Product: {product_name:15} Price: ₡{product_price:>10}\n"
                total_price += product[1]
            else:
                summary += f"Product: {product_name:15} Not Available\n"
        
        summary += "\n" + "=" * 30 + "\n"
        summary += f"Total Price: ₡{total_price:>10}"
        
        messagebox.showinfo("Sale Summary", summary)

    def placeOrder(self, products, quantities):
        saleProducts = []
        for quantity in quantities:
            q =  int(quantity.get())
            if (q>0):
                product = products[quantities.index(quantity)]
                # print(product[1], quantity.get());
                productId = product[0]
                totalPrice = float(str(product[2])) * quantity.get()

                queryAvailable = "Select top 1 inventoryProduct.quantity FROM inventoryProduct WHERE productId = ?"
                available = executeQuery(connection, queryAvailable, [productId], 0)
                if (available[0][0] >= q):
                    data = executeQuery(connection, execProc, [productId, totalPrice, q], 1)
                    saleProducts.append([product[1], totalPrice, True])
                else:
                    saleProducts.append([product[1], 0, False])
        self.showSummary(saleProducts)

    # Check Info
    def checkInfo(self):
        if self.infoSection:
            self.infoSection.destroy()
            self.infoSection.grid_forget()
            self.infoSection = None
        else:
            # Create Section
            self.infoSection = ctk.CTkScrollableFrame(self,
                            label_text="Participants Information")
            self.infoSection.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            self.infoSection.grid_columnconfigure(0, weight=1)
            ## Get data
            titles = ["Participants", "Collectors", "Producers"]
            colors = ["#2CC985", "white", "#2CC985"]
            row = 0
            for query in queries:
                index = queries.index(query)
                data = executeQuery(connection, query, [1], 0) # change 1 for the contract id
                titleLabel = ctk.CTkLabel(self.infoSection, text=titles[index], font=("Arial", 20, "bold"), text_color=colors[index])
                titleLabel.grid(row=row, column=0, padx=10, pady=(0, 20), sticky="w", rowspan=len(data)-1)
                for i in range(len(data)):
                    info = "ID: " + str(data[i][0]) + "\nName: " + str(data[i][1]) + "\nBalance: " + str(data[i][2]) + "\nPercentage: " + str(data[i][3])
                    infoLabel = ctk.CTkLabel(self.infoSection, text=info, text_color=colors[index])
                    infoLabel.grid(row=row, column=1, padx=10, pady=(0, 20), sticky="w")
                    row += 1




# -----------------------------------------------
# FUNCTIONS
def connect():
    server = 'localhost'
    database = 'caso3'
    cnxn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION=yes;')

    return cnxn

def executeQuery(cnxn, query, params, proc):
    cursor = cnxn.cursor()
    try:
        if params == [] and proc:
            # print("executing proc")
            cursor.execute(query)
            connection.commit()
            return
        elif params == [] and not proc:
            # print("executing query")
            cursor.execute(query)
            return cursor.fetchall()
        if params != [] and proc:
            # print("executing proc with params")
            cursor.execute(query, params)
            connection.commit()
            return
        else:
            # print("executing query with params")
            cursor.execute(query, params)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
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


#Execute Queries
procedure = """
alter PROCEDURE [dbo].[registerSales] 
        @client INT,
        @product INT,
        @seller INT,
        @totalPrice DECIMAL(12,2),
        @paymentType INT,
        @contract INT,
		@quantity INT
    AS
    BEGIN 

        DECLARE @sellerPercentage decimal(5,2);
        DECLARE @producerPercentage decimal(5,2);
        DECLARE @collectorPercentage decimal(5,2);
		DECLARE @availableStock int;

		set @availableStock = (Select top 1 inventoryProduct.quantity FROM inventoryProduct WHERE productId = @product);

		IF(@availableStock >= @quantity) 
		BEGIN
			UPDATE inventoryProduct SET quantity = quantity - @quantity WHERE productId = @product; 

        INSERT INTO [dbo].[sales]([clientId], [productId], [sellerId], [totalPrice], [posttime], [checksum], [paymentTypeId], [contractId], [quantity]) VALUES
            (@client, @product, @seller, @totalPrice, GETDATE(), NULL, @paymentType, @contract, @quantity);


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
    END;
"""
execProc = """
    exec registerSales @client =1,
        @product =?,
        @seller =1,
        @totalPrice = ?,
        @paymentType = 1,
        @contract =1,
        @quantity = ?;
"""

# print("1")
# Create Procedure To Register Sales
executeQuery(connection, procedure, [], 1)
# print("2")
# Select Products for the app
queryProducts = "SELECT * FROM products"
products = executeQuery(connection, queryProducts, [], 0)

app = App(products)
app.mainloop()


connection.close()
