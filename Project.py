from Animation import Animation

class Project(object):
    def __init__(self, name:str) -> None:
        self.name = name
        self.animations = {}

    def addAnimation(self, name):
        print("animation added")
        self.animations[str(name)] = Animation(name)
        

    def getAnimation(self,name):
        return self.animations[name]

    def saveAnimation(self, animation):
        self.animations[str(animation.name)] = animation