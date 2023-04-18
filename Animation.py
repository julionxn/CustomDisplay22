#Animation class
class Animation():
    def __init__(self, name) -> None:
        self.name = name
        self.frames = {}
        self.options = {"type":"autogen", "scale":1, "height":1}
        self.sound = ""
        self.size = [0,0]
        