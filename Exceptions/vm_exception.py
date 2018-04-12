class VMException(Exception):
    def __init__(self, body):
        super()
        self.error = "Error is " + body