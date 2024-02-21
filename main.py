import customtkinter


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("system")
        self.title = "Password Manager"
        self.geometry("1280x720")

        ## Grid Config
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1 ,2), weight=10)

        ## Main Srollframe
        self.scrollframe = ScrollFrame(master=self)
        self.scrollframe.grid(row=1, column=0, sticky="nesw", columnspan=5, rowspan=2, padx=15, pady=15)
        
        ## Button to Edit List
        self.createButton = customtkinter.CTkButton(self, text="Create New", height=30, command=self.newEntry, fg_color="green").grid(row=0, column=3, padx=20, pady=15)
        self.deleteButton = customtkinter.CTkButton(self, text="Delete", height=30, command=self.deleteEntry, fg_color="red").grid(row=0, column=4, padx=20, pady=15)

        ## Entry Box
        self.entrybox = customtkinter.CTkEntry(self, placeholder_text="Insert you Accountname", height=30)
        self.entrybox.grid(row=0, column=0, padx=50, columnspan=3, sticky="we")
        
    def newEntry(self):
        if self.entrybox.get() == "":
            print(f"Please enter a name for the entry.")
        else:
            self.scrollframe.add_item(self.entrybox.get())

    def deleteEntry(self):
        if self.entrybox == "":
            print(f"Please enter a name for the entry.")
        else:
            self.scrollframe.remove_item(self.entrybox.get())



## Main Srollframe
class ScrollFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1), weight=1)

        self.labellist = []
        self.buttonlist = []

    def add_item(self, item):
        label = customtkinter.CTkLabel(self, text=item, width=800, height=50).grid(row=len(self.labellist), column=0, padx=10, pady=10)
        button = customtkinter.CTkButton(self, text=item, width=280, height=50, command=self.buttonCommand, hover=True).grid(row=len(self.buttonlist), column=1, padx=10, pady=10)
        self.labellist.append(label)
        self.buttonlist.append(button)

    def remove_item(self, item):
        for label, button in zip(self.labellist, self.buttonlist):
            if item == label.cget("text"):
                label.destroy()
                button.destroy
                self.labellist.remove(label)
                self.buttonlist.remove(button)
                return

    def buttonCommand(self):
        print("Button clicked!")

        #self.label = customtkinter.CTkLabel(self, text="No 1", width=50, height=25).grid(row=1, column=0)
        #self.button = customtkinter.CTkButton(self, text="No 1", width=50, height=25).grid(row=1, column=1)



app = App()
app.mainloop()