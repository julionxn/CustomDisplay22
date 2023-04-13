import customtkinter as tk
import Project
from scrollProjects import ScrollableLabelButtonFrame
from newAnimationScreen import NewAnimationScreen
from animationScreen import AnimationScreen
from helper import saveProject
from generate import generate
from popupWindow import PopupWindow

class ProjectScreen(tk.CTkToplevel):
    def __init__(self, master, project:Project.Project, new: bool):
        super().__init__(master)
        self.project = project
        self.title(self.project.name + " Project")
        self.geometry("500x370")
        self.geometry("+%d+%d" %(master.winfo_x(),master.winfo_y()))
        self.resizable(False,False)

        self.label = tk.CTkLabel(self, text=self.project.name + " Animations", font=("Roboto",30))
        self.label.pack(pady=10)

        def openAnimation(animation):
            AnimationScreen(self,self.project,self.project.animations[str(animation)])

        self.frame = ScrollableLabelButtonFrame(self, width=400,height=200, command=openAnimation)
        self.frame.place(x=30,y=105)

        if bool:
            for i in list(project.animations.keys()):
                self.frame.add_item(i)
        
        def save():
            saveProject(f"{self.project.name}.cd22",self.project)

        def addAnimation():
            NewAnimationScreen(self)

        self.add = tk.CTkButton(self, text="Save", font=("Roboto",16),width=28, command=save)
        self.add.pack()

        self.add = tk.CTkButton(self, text="+", font=("Roboto",20),width=28, command=addAnimation)
        self.add.place(x=460,y=105)

        def gen():
            save()
            generate(self.project)
            PopupWindow(self, "Listo", "Se ha generado tu proyecto.")


        self.gen = tk.CTkButton(self, text="Generate", font=("Roboto",16), command=gen)
        self.gen.place(x=180,y=330)

        def on_closing():
            save()
            master.destroy()

        self.protocol("WM_DELETE_WINDOW", on_closing)
        