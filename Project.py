from Animation import Animation

class Project(object):
    def __init__(self, name:str) -> None:
        self.name = name
        self.version = "1.2"
        self.animations = {}

    def getAnimation(self,name):
        return self.animations[name]

    def saveAnimation(self, animation):
        self.animations[str(animation.name)] = animation