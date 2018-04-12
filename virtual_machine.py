import paramiko
import SETTINGS
from Exceptions.vm_exception import VMException


class virtual_machine:
    def __init__(self):
        self.mac = ""
        self.ip = ""
        self.xml = ""
        self.name = ""
        self.image = ""
        self.domain = None
        self.ssh = None

    def open_ssh(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.ip, username=SETTINGS.USER, password=SETTINGS.PASSWORD, port=22)

    def send_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        # print(stderr.read().decode('utf-8'))
        # if stderr.read().decode('utf-8') is not "":
        #     raise VMException(stderr.read().decode('utf-8'))
        return stdout.read().decode('utf-8')