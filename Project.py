from Animation import Animation

class Project(object):
    def __init__(self, name:str) -> None:
        self.name = name
        self.animations = {}

    def addAnimation(self, name):
        self.animations[name] = Animation(name)
        print("animation added")

    def getAnimation(self,name):
        return self.animations[name]

    def saveAnimation(self, animation):
        self.animations[str(animation.name)] = animation