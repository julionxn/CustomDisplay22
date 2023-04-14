import Project
from shutil import rmtree, copytree, copy
from os import mkdir
from helper import loadJson, dumpJson, genFunc
import os
import glob
from PIL import Image, ImageDraw
from shutil import copyfile

#Project structure:
#   name: str
#   animations -> (str) name : (Animation) animation
#       animation:
#           name: str
#           frames -> (str) numberFrame : (str) filename
#           options -> (str)type, (int)scale, (int)height
#               type: autogen || custom
#           size: (int, int)

def generate(project: Project.Project) -> None:
    pName = project.name
    animations = project.animations
    genRootFolders(pName)
    genResourcePack(pName, animations)
    genDatapack(pName, animations)


def genRootFolders(pName):
    try:
        rmtree(f"./.output/{pName}")
    except:
        pass
    mkdir(f"./.output/{pName}")
    copytree("./src/preset/rp", f"./.output/{pName}/{pName}-ResourcePack")
    copytree("./src/preset/dp", f"./.output/{pName}/{pName}-Datapack")


#default.json structure:
# {
# "providers":[
#     {
#       "type": "bitmap",
#       "file": "minecraft:animations/ANIMATION_NAME/frame"
#       "ascent": height / 2
#       "height": gen,
#       "chars": ["char"] <- "\uE030"
#     }
#   ]
# }

def genResourcePack(pName, animations):
    place = 57392
    defaultJsonFile = f"./.output/{pName}/{pName}-ResourcePack/assets/minecraft/font/default.json"
    soundsJsonFile = f"./.output/{pName}/{pName}-ResourcePack/assets/minecraft/sounds.json"
    default = loadJson(defaultJsonFile)
    sounds = loadJson(soundsJsonFile)
    for name in list(animations.keys()):
        animation = animations[name]
        animationOpts = animation.options
        animationH = animation.size[1]
        sound = animation.sound
        if sound not in [" ",""]:
            animationSoundSource = f"./.projects/{pName}/{name}/{sound}"
            animationSoundDest = f"./.output/{pName}/{pName}-ResourcePack/assets/minecraft/sounds/asounds/{sound}"
            copyfile(animationSoundSource,animationSoundDest)
            sounds[f"{pName}.{sound[:-4]}"] = {"sounds": [f"asounds/{sound[:-4]}"]}
            dumpJson(soundsJsonFile, sounds)
        #frames
        jsonPath = f"minecraft:animations/{name}"
        animationDestPath = f"./.output/{pName}/{pName}-ResourcePack/assets/minecraft/textures/animations/{name}"
        animationSourcePath = f"./.projects/{pName}/{name}"
        mkdir(animationDestPath)
        #copy frames
        for frame in glob.iglob(os.path.join(animationSourcePath, "*.png")):
            copy(frame, animationDestPath)
        #add each frame to default.json
        for key in list(animation.frames.keys()):
            frameFile = animation.frames[str(key)]

            #open frame, add pixels to correct centering, and into de the textures/animations folder
            img = Image.open(f"{animationSourcePath}/{frameFile}")
            draw = ImageDraw.Draw(img)
            draw.point(((0,0),(img.width-1,img.height-1)),(0,0,0,1))
            img.save(f"{animationDestPath}/{frameFile}")

            bp = {"type": "bitmap",
                "file": f"{jsonPath}/{frameFile}",
                "ascent": 0,
                "height": 0,
                "chars": [chr(place)]
                }
            if animationOpts["type"] == "autogen":
                scale = animationOpts["scale"]
                height = int((animationH*scale)/8)
            elif animationOpts["type"] == "custom":
                height = animationOpts["height"]
            bp["height"] = height
            bp["ascent"] = int(height/2)
            default["providers"].append(bp)
            place += 1
    dumpJson(defaultJsonFile, default)


def genDatapack(pName, animations):
    place = 57392
    path = f"./.output/{pName}/{pName}-Datapack/data/"
    os.mkdir(f"{path}/{pName}")
    os.mkdir(f"{path}/{pName}/functions")
    for name in list(animations.keys()):
        animation = animations[name]
        #make folder for the animation
        functionPath = f"./.output/{pName}/{pName}-Datapack/data/{pName}/functions/{name}"
        mkdir(functionPath)
        #make starting function for the animation
        animationSoundFile = animation.sound
        if animationSoundFile not in [" ",""]:
            lines = [f"tag @s add cd22_{pName}_{name}_0",
                    f"title @s times 0 2 0",
                    f"execute as @s at @s run playsound minecraft:{pName}.{os.path.basename(animationSoundFile)[:-4]} master @s ~ ~ ~ 1 1 1",
                    f"schedule function {pName}:{name}/0 1t"]
        else:
            lines = [f"tag @s add cd22_{pName}_{name}_0",
                    f"title @s times 0 2 0",
                    f"schedule function {pName}:{name}/0 1t"]
        genFunc(f"./.output/{pName}/{pName}-Datapack/data/{pName}/functions/_{name}.mcfunction", lines)
        lines = ["title @a[tag=cd22_final] reset",
                 "tag @a[tag=cd22_final] remove cd22_final"]
        genFunc(f"./.output/{pName}/{pName}-Datapack/data/{pName}/functions/reset.mcfunction", lines)
        #make the function for each frame
        for key in list(animation.frames.keys()):
            data = {"text": f"{chr(place)}"}
            if int(key) < len(list(animation.frames.keys())) - 1:
                lines = [
                f"execute as @a[tag=cd22_{pName}_{name}_{key}] run title @s title {data}".replace("\'","\""),
                f"tag @a[tag=cd22_{pName}_{name}_{key}] add cd22_{pName}_{name}_{int(key)+1}",
                f"tag @a[tag=cd22_{pName}_{name}_{key}] remove cd22_{pName}_{name}_{key}",
                f"schedule function {pName}:{name}/{int(key)+1} 1t"
            ]
            else:
                lines = [
                f"execute as @a[tag=cd22_{pName}_{name}_{key}] run title @s title {data}".replace("\'","\""),
                f"tag @a[tag=cd22_{pName}_{name}_{key}] add cd22_final",
                f"tag @a[tag=cd22_{pName}_{name}_{key}] remove cd22_{pName}_{name}_{key}",
                f"schedule function {pName}:reset 1t"
            ]
                

            genFunc(f"./.output/{pName}/{pName}-Datapack/data/{pName}/functions/{name}/{key}.mcfunction", lines)
            place += 1
            

