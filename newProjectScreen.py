import customtkinter as tk
from Project import Project
from helper import saveProject
from projectScreen import ProjectScreen
import os
from re import match

class NewProjectScreen(tk.CTkToplevel):
    def __init__(self, master: tk.CTk):
        super().__init__(master)
        self.geometry("250x100")
        self.title("New Project")
        self.resizable(False,False)

        self.label = tk.CTkLabel(self, text="New Project Name")
        self.label.pack()

        #Check if the entry is valid
        def check(P):
            return bool(match("^[a-z0-9_]*$", str(P)))
        vcmd = (self.register(check))

        #Name entry
        self.entry = tk.CTkEntry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.entry.pack()

        #Create project
            #Behaviour
        def createProject():
            name = self.entry.get()
            try:
                os.mkdir(f"./.projects/{name}")
            except Exception:
                pass
            new = Project(name)
            saveProject(f"{name}.cd22", new)
            ProjectScreen(master,new,True)
            
            self.destroy()

            #Button
        self.button = tk.CTkButton(self, text="Create", command= lambda: createProject())
        self.button.pack(pady=5)

        #Window behaviour
        self.geometry("+%d+%d" %(master.winfo_x()+125,master.winfo_y()+50))
        master.withdraw()

        #Closing
        def on_closing():
            master.deiconify()
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", on_closing)
            

    