import dotenv
import os
import customtkinter
import mysql.connector
from PIL import Image

dotenv.load_dotenv()

mydb = mysql.connector.connect(
  host=os.getenv('DB_HOST'),
  port=os.getenv('DB_PORT'),
  user=os.getenv('DB_USER'),
  password=os.getenv('DB_PASSWORD')
)

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("dark")
        self.title("Password Manager")
        self.geometry("1280x720")

        self.darkmode = True
        self.newEntryDialog = None

        ## Grid Config
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1 ,2), weight=10)

        ## Main Srollframe
        self.scrollframe = ScrollFrame(master=self)
        self.scrollframe.grid(row=1, column=0, sticky="nesw", columnspan=5, rowspan=2, padx=15, pady=15)
        
        ## Button to Edit List
        mondImage = customtkinter.CTkImage(dark_image=Image.open("assets/moon-light.png"), light_image=Image.open("assets/moon-dark.png"), size=(30, 30))
        self.createButton = customtkinter.CTkButton(self, text="Create New", height=30, command=self.newEntry, fg_color="green")
        self.createButton.grid(row=0, column=4, padx=20, pady=15, sticky="w")
        self.darkMode = customtkinter.CTkButton(self, text="DarkMode", height=30, image=mondImage, command=self.toggleDarkMode)
        self.darkMode.grid(row=0, column=4, padx=20, pady=15, sticky="e")

    def toggleDarkMode(self):
        if self.darkMode:
            customtkinter.set_appearance_mode("light")
            self.darkMode = False
        else:
            customtkinter.set_appearance_mode("dark")
            self.darkMode = True

    def getDarkMode(self):
        return self.darkMode

    def newEntry(self):
        if self.newEntryDialog is None or not self.newEntryDialog.winfo_exists():
            self.newEntryDialog = EntryDialog(self)
        else:
            self.newEntryDialog.focus()

    def newEntryold(self):
        if self.entrybox.get() == "":
            print(f"Please enter a name for the entry.")
        else:
            self.scrollframe.add_item(self.entrybox.get())

    def deleteEntry(self):
        if self.entrybox == "":
            print(f"Please enter a name for the entry.")
        else:
            self.scrollframe.remove_item(self.entrybox.get())


class EntryDialog(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        ## CONFIRM BUTTON
        self.button = customtkinter.CTkButton(self, text="Confirm", height=30, fg_color="green", command=self.confirmPressed)
        self.button.grid(row=3, column=1, padx=30, sticky="e")
        ## CANCEL BUTTON
        self.button = customtkinter.CTkButton(self, text="Cancel", height=30, fg_color="red", command=self.cancelPressed)
        self.button.grid(row=3, column=1, padx=30, sticky="w")

        ## AccountName Field
        self.accountNameField = customtkinter.CTkEntry(self, width=350, placeholder_text="Account Name")
        self.accountNameField.grid(row = 0, column = 1)
        ## Name Field
        self.nameField = customtkinter.CTkEntry(self, width=350, placeholder_text="Name")
        self.nameField.grid(row = 1, column = 1)
        ## Password Field
        self.passwordField = customtkinter.CTkEntry(self, width=350, placeholder_text="Password", show="*")
        self.passwordField.grid(row = 2, column = 1)

    def confirmPressed(self):
        print("Confirm")
        self.account = self.accountNameField.get()
        self.name = self.nameField.get()
        self.password = self.passwordField.get()
        print(self.account, self.name, self.password)   ## Create SQL Entry and refresh list

    def cancelPressed(self):
        print("Cancel")


## Main Srollframe
class ScrollFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0), weight=1)

        self.framelist = []
        self.labellist = []
        self.buttonlist = []

    def add_item(self, item):
        frame = customtkinter.CTkFrame(self, width=200, height=200, fg_color="#424242")
        frame.grid(sticky="nsew", column=0, padx=10, pady=10)
        frame.grid_columnconfigure((0,1), weight=1)
        label = customtkinter.CTkLabel(frame, text=item, width=800, height=50, )
        label.grid(row=len(self.labellist), column=0, padx=10, pady=10)
        button = customtkinter.CTkButton(frame, text="Action", width=280, height=50, command=self.buttonCommand, hover=True)
        button.grid(row=len(self.buttonlist), column=1, padx=10, pady=10)
        self.framelist.append(frame)
        self.labellist.append(label)
        self.buttonlist.append(button)

    def remove_item(self, item):
        for frame, label, button in zip(self.framelist, self.labellist, self.buttonlist):
            print(label, button)
            if item == label.cget("text"):
                frame.destroy()
                label.destroy()
                button.destroy()
                self.framelist.remove(frame)
                self.labellist.remove(label)
                self.buttonlist.remove(button)
                return

    def buttonCommand(self):
        print("Button clicked!")

app = App()
app.mainloop()