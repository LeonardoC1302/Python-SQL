import tkinter
import tkinter.messagebox
import customtkinter as ctk
from PIL import Image as img
from typing import Union, Callable

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

class FloatSpinbox(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

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
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            if value >= 0:  # check that value is positive
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
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

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title('Register Sales')
        self.geometry(f"{1100}x{580}")
        
        # create 2x2 grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, minsize=20)
        self.rowconfigure(1, weight=1)

        # Window main label (Title)
        textTitle = tkinter.StringVar(value="Buy Your Products")
        labelTitle = ctk.CTkLabel(self,
                                textvariable=textTitle,
                                width=10,
                                height=1,
                                fg_color="transparent",
                                text_color=("black", "white"),
                                font=("Arial", 30, "bold"),
                                corner_radius=8)
        labelTitle.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        # Add side image
        sideImage = ctk.CTkImage(light_image=img.open("img/darkImg.png"),
                                dark_image=img.open("img/darkImg.png"),
                                size=(200, 200))

        button = ctk.CTkButton(self, image=sideImage, text="", fg_color="transparent", bg_color="transparent", state="disabled")
        button.grid(row=1, column=0, sticky="nsew", columnspan=1, rowspan=3)

        # Add form
        scrollFrameProducts = ctk.CTkScrollableFrame(self,
                            label_text="Select Your Products")
        scrollFrameProducts.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        scrollFrameProducts.grid_columnconfigure(0, weight=1)
        ## Add products
        products = [(1,"Zapato"), (2, "Mesa"), (3, "Silla")] # list of products from SQL
        checkVarsP = []
        for i in range(len(products)-1):
            checkVar = tkinter.StringVar(value="off")
            checkVarsP.append(checkVar)
            checkbox = ctk.CTkCheckBox(scrollFrameProducts,
                                text = products[i][1],
                                variable = checkVar,
                                onvalue="on",
                                offvalue="off")
            checkbox.grid(row=i, column=0, padx=10, pady=(0, 20))

        ## Select Quantity of products
        scrollFrameQuantity = ctk.CTkScrollableFrame(self,
                            label_text="Select Your Quantity")
        scrollFrameQuantity.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        scrollFrameQuantity.grid_columnconfigure(0, weight=1)
        scrollFrameQuantity.grid_columnconfigure(1, weight=1)

        spinboxesP = []
        for i in range(len(products)-1):
            spinbox = FloatSpinbox(scrollFrameQuantity, width=150, step_size=1, )
            spinboxesP.append(spinbox)
            spinbox.grid(row=i, column=1, padx=10, pady=(0, 20), sticky="w")
            spinboxLabel = ctk.CTkLabel(scrollFrameQuantity, text=products[i][1])
            spinboxLabel.grid(row=i, column=0, padx=10, pady=(0, 20), sticky="e")

        ## Submit button
        buttonSubmit = ctk.CTkButton(self,
                                    fg_color="transparent",
                                    border_width=2,
                                    text_color=("gray10", "#DCE4EE"),
                                    corner_radius=30,
                                    text="Submit Order") #Add command
        buttonSubmit.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)
app = App()
app.mainloop()