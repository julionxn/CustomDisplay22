import customtkinter as tk
from Project import Project
from helper import saveProject
from animationScreen import AnimationScreen
from Animation import Animation
import os
from re import match

class NewAnimationScreen(tk.CTkToplevel):
    def __init__(self, tl):
        super().__init__(tl)
        self.geometry("250x100")
        self.title("New Project")
        self.resizable(False,False)

        self.label = tk.CTkLabel(self, text="New Animation Name")
        self.label.pack()

        def check(P):
            return bool(match("^[a-z0-9_]*$", str(P)))
        vcmd = (self.register(check))

        self.entry = tk.CTkEntry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.entry.pack()

        def createAnimation():
            name = self.entry.get()
            try:
                os.mkdir(f"./.projects/{tl.project.name}/{name}")
            except Exception:
                pass
            tl.project.saveAnimation(Animation(name))
            anim = tl.project.getAnimation(name)
            tl.frame.add_item(name)
            AnimationScreen(tl,tl.project, anim)
            self.destroy()

        self.button = tk.CTkButton(self, text="Create", command= lambda: createAnimation())
        self.button.pack(pady=5)
        self.geometry("+%d+%d" %(tl.winfo_x()+125,tl.winfo_y()+50))
        tl.withdraw()

        def on_closing():
            tl.deiconify()
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", on_closing)
            

    