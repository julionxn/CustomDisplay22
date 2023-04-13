from PIL import Image

class Animation():
    def __init__(self, name) -> None:
        self.name = name
        self.frames = {}
        self.options = {"type":"autogen", "scale":1, "height":1}
        self.size = [0,0]
        