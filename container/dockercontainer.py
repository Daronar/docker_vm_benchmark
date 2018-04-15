import SETTINGS
import time

class DockerContainer:
    def __init__(self):
        self.name = ""
        self.image = ""
        self.container = None
        self.cpu_set = ""

    def send_cmd_without_answer(self, cmd):
        full_cmd = 'bash -c "%s"'%cmd
        print("cmd for " + self.name + " without answer " + full_cmd)
        self.container.exec_run(cmd=full_cmd, detach=True, tty=True)

    def send_cmd(self, cmd):
        full_cmd = 'bash -c "%s"'%cmd
        print("cmd for " + self.name + " " + full_cmd)
        stdout = self.container.exec_run(cmd=full_cmd, tty=True)
        # print(int(time.time() - cur_time))
        return stdout[1].decode("utf-8")
