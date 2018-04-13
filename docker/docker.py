import SETTINGS

class DockerContainer:
    def __init__(self):
        self.name = ""
        self.image = ""
        self.container = None
        self.cpu_set = ""

