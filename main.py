import customtkinter as tk
from PIL import Image
import os
from scrollProjects import ScrollableLabelButtonFrame
from helper import readProject
from newProjectScreen import NewProjectScreen
from projectScreen import ProjectScreen
from os import listdir
from os.path import isfile, join


tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")

root = tk.CTk()
root.title("Custom Display 22")
root.resizable(False,False)

width = 500
height = 370 
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() 
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
 
root.geometry('%dx%d+%d+%d' % (width, height, x, y))


image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "src")
home_image = tk.CTkImage(light_image=Image.open(os.path.join(image_path, "LogoName.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "LogoName.png")), size=(232/1.5, 92/1.5))
label = tk.CTkLabel(root, text="", image=home_image)
label.place(x=30,y=60)

def newProject():
    NewProjectScreen(root)

version = tk.CTkLabel(root, text="v1.1", font=("Roboto",12))
version.place(x=100,y=220)

newB = tk.CTkButton(root, text="New Project",command=newProject)
newB.place(x=40,y=140)
    

newB = tk.CTkButton(root, text="Import Project")
newB.place(x=40,y=180)

def openProject(name):
    project = readProject(f"{name}.cd22")
    ProjectScreen(root, project, True)
    root.withdraw()

frame = ScrollableLabelButtonFrame(root,width=240,height=300,command=openProject)
frame.place(x=220,y=30)

try:
    os.mkdir("./.projects")
except:
    pass
try:
    os.mkdir("./.output")
except:
    pass

projects = [f for f in listdir("./.projects/") if isfile(join("./.projects/", f))]
for i in projects:
    frame.add_item(readProject(i).name)






root.mainloop()