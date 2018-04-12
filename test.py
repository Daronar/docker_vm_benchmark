import importlib

class Test:
    def __init__(self):
        self.name = ""
        self.install_cmd = ""
        self.run_cmd = ""
        self.result_cmd = ""
        self.execution_time = 0
        self.result_function = None

    def load(self, file_name):
        t = importlib.import_module(file_name)
        self.name = t.name
        self.install_cmd = t.install_cmd
        self.run_cmd = t.run_cmd
        self.result_cmd = t.result_cmd
        self.execution_time = t.execution_time
        self.result_function = t.result_function


t = Test()
t.load('examples.john-the-ripper')
print(t.name)
