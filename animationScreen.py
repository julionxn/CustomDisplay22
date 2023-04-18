import customtkinter as tk
import Animation
import Project
from os import listdir, getcwd
from os.path import isfile, join, abspath
from PIL import Image
import tkinter as tkk
from re import match
from subprocess import Popen

class AnimationScreen(tk.CTkToplevel):
    def __init__(self, master, project:Project.Project, animation:Animation.Animation):
        super().__init__(master)
        self.project = project
        self.animation = animation
        self.title(self.project.name + " -> " + self.animation.name)
        self.frames = {}
        self.currentFrame = 0
        self.loadedSound = True if self.animation.sound != "" else False
        self.geometry("500x380")
        self.geometry("+%d+%d" %(master.winfo_x(),master.winfo_y()))
        self.resizable(False,False)

        #=========Preview===========#
        ##Frame (Just visual)
        self.framesFrame = tk.CTkFrame(self,width=360,height=380,corner_radius=0)
        self.framesFrame.place(x=0,y=0)

        #Title of the aniamtion
        self.label = tk.CTkLabel(self, text=self.animation.name, font=("Roboto",30),width=360,bg_color="#212121")
        self.label.place(x=0,y=10)

        #Button to load data (Frames and sound)
        self.load = tk.CTkButton(self, text="Load Data", command=self.loadData, width=100)
        self.load.place(x=160,y=70)

        #Open folder of the animation
        self.openFolder = tk.CTkButton(self, text="Folder", command=self.openFolder,width=70)
        self.openFolder.place(x=70, y=70)

        #Preview Window
            #Default
        self.defaultPreview = Image.open("./src/defaultPreview.png")
        self.previewImg = tk.CTkImage(dark_image=self.defaultPreview, size=(320,180))
        self.preview = tk.CTkLabel(self, image=self.previewImg, text="")
        self.preview.place(x=20,y=110)

        #Next frame button and behaviour
        def nextFrame():
            if (self.currentFrame + 1 < len(list(self.frames.keys())) - 1):
                self.currentFrame += 1
                self.preview.configure(image=self.getPreview(self.currentFrame))

        self.next = tk.CTkButton(self, text=">", width=28, command=nextFrame)
        self.next.place(x=200,y=300)

        #Previous frame button and behaviour
        def prevFrame():
            if (self.currentFrame - 1 != -1):
                self.currentFrame -= 1
                self.preview.configure(image=self.getPreview(self.currentFrame))

        self.next = tk.CTkButton(self, text="<", width=28, command=prevFrame)
        self.next.place(x=130,y=300)

        #Feedback label
        self.labelfb = tk.CTkLabel(self, text="", bg_color="#212121", width=360, anchor=tk.CENTER)
        self.labelfb.place(x=0,y=340)


        #=========Options===========#

        #vars
        self.type = tkk.IntVar()
        self.type.set(0)
        self.type_scale = tkk.StringVar()
        self.type_scale.set(str(self.animation.options["scale"]))
        self.type_height = tkk.StringVar()
        self.type_height.set(str(self.animation.options["height"]))

        #options label
        self.labels = tk.CTkLabel(self, text="Options")
        self.labels.place(x=410,y=80)

        #Scale entry
            #behaviour
        def autosize():
            self.animation.options["type"] = "autogen"
            self.entry_scale.configure(state="normal")
            self.entry_height.configure(state="disabled")
            self.reload()

            #Button
        self.autogen = tk.CTkRadioButton(self, text="Auto-size", variable=self.type, value=0, command=autosize)
        self.autogen.place(x=380,y=120)

            #Label
        self.txt_scale = tk.CTkLabel(self, text="Scale: ")
        self.txt_scale.place(x=380,y=150)

            #Check if the entry is digit
        def check(P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False
        vcmd = (self.register(check))

            #Entry
        self.entry_scale = tk.CTkEntry(self, textvariable=self.type_scale, justify=tkk.CENTER, width=50, validate='all', validatecommand=(vcmd, '%P'))
        self.entry_scale.place(x=430,y=150)

        #Height entry
            #Behaviour
        def autoheight():
            self.animation.options["type"] = "custom"
            self.entry_scale.configure(state="disabled")
            self.entry_height.configure(state="normal")
            self.reload()

            #Button
        self.custom = tk.CTkRadioButton(self, text="Custom", variable=self.type, value=1, command=autoheight)
        self.custom.place(x=380,y=220)

            #Label
        self.txt_height = tk.CTkLabel(self, text="Height: ")
        self.txt_height.place(x=380,y=250)

            #Entry
        self.entry_height = tk.CTkEntry(self, textvariable=self.type_height, justify=tkk.CENTER, width=50, validate='all', validatecommand=(vcmd, '%P'))
        self.entry_height.place(x=430,y=250)


        #Reload when changing valuos of scale or height
        def callback(ctx):
            self.reload()

        self.type_scale.trace("w", lambda name, index,mode, type_scale=self.type_scale: callback(type_scale))
        self.type_height.trace("w", lambda name, index,mode, type_height=self.type_height: callback(type_height))

        #Load data
        if self.animation.options["type"] == "autogen":
            self.entry_scale.configure(state="normal")
            self.entry_height.configure(state="disabled")
        elif self.animation.options["type"] == "custom":
            self.entry_scale.configure(state="disabled")
            self.entry_height.configure(state="normal")
        self.loadData()

        ###CLOSING
        master.withdraw()

        def on_closing():
            print("called")
            self.project.animations[self.animation.name] = self.animation
            master.deiconify()
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", on_closing)

    def loadData(self):
            frameImages = [f for f in listdir(f"./.projects/{self.project.name}/{self.animation.name}/") if f.endswith(".png") and isfile(join(f"./.projects/{self.project.name}/{self.animation.name}/", f))]
            animSound = [f for f in listdir(f"./.projects/{self.project.name}/{self.animation.name}/") if f.endswith(".ogg") and isfile(join(f"./.projects/{self.project.name}/{self.animation.name}/", f))]
            frameImages = tkk.Tcl().call('lsort', '-dict', frameImages)
            for index, frame in enumerate(frameImages):
                self.frames[str(index)] = frame
            self.animation.frames = self.frames
            if len(animSound) > 0:
                if bool(match("^[a-z0-9_]*$", str(animSound[0][:-4]))):
                    self.animation.sound = animSound[0]
                    state = True
                else:
                    state = False
            else:
                state= True
                self.animation.sound = ""
            try:
                pilimg = Image.open(f"./.projects/{self.project.name}/{self.animation.name}/{self.frames[str(0)]}")
                self.animation.size[0] = pilimg.width
                self.animation.size[1] = pilimg.height
                self.preview.configure(image=self.getPreview(0))
            except:
                self.labelfb.configure(text="Error while reading frames")
            if state:
                if len(frameImages) > 0:
                    if len(animSound) > 0:
                        self.labelfb.configure(text="Frames and sound loaded")
                    else:
                        self.labelfb.configure(text="Frames loaded")
                else:
                    self.labelfb.configure(text="Frames not founded")
            else:
                self.labelfb.configure(text="Invalid sound filename")

    def openFolder(self):
            path = f"{abspath(getcwd())}\.projects\{self.project.name}\{self.animation.name}\\"
            Popen(fr"explorer {path}")

    def getPreview(self,index):
        img = Image.open(f"./.projects/{self.project.name}/{self.animation.name}/{self.frames[str(index)]}")
        if self.animation.options["type"] == "autogen":
            scale = int(self.animation.options["scale"])
            img = img.resize((int((img.width * 320 / 1239)*scale), int((img.height * 180 / 697)*scale)), resample=Image.NEAREST)
        elif self.animation.options["type"] == "custom":
            scale = int(self.animation.options["scale"])
            img = img.resize((int((img.width * 320 / 1239)*scale), int((img.height * 180 / 697)*scale)), resample=Image.NEAREST)

        default = Image.open("./src/defaultPreview.png")
        default.paste(img, (int((320-img.width)/2),int((180-img.height)/2)), img)

        return tk.CTkImage(dark_image=default, size=(320,180))
    
    def reload(self):
            if self.animation.options["type"] == "autogen" and self.type_scale.get() not in [" ", ""]:
                try:
                    newscale = int(self.type_scale.get())
                    self.animation.options["scale"] = newscale
                    self.preview.configure(image=self.getPreview(self.currentFrame))
                    self.type_scale.set(str(newscale))
                except ValueError:
                    pass
            elif self.animation.options["type"] == "custom" and self.type_height.get() not in [" ", ""]:
                try:
                    height = int(self.type_height.get())
                    newscale = int((8*height)/self.animation.size[1])
                    self.animation.options["scale"] = newscale
                    self.animation.options["height"] = height
                    self.preview.configure(image=self.getPreview(self.currentFrame))
                    self.type_scale.set(str(newscale))
                    self.type_height.set(str(height))
                except:
                    pass