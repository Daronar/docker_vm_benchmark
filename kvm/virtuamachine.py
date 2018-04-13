import paramiko
import SETTINGS
from Exceptions.vm_exception import VMException


class VirtuaMachine:
    def __init__(self):
        self.mac = ""
        self.ip = ""
        self.xml = ""
        self.name = ""
        self.image = ""
        self.domain = None
        self.ssh = None
        self.cpu_set = ""

    def open_ssh(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.ip, username=SETTINGS.USER, password=SETTINGS.PASSWORD, port=22)

    def send_cmd_without_answer(self, cmd):
        self.ssh.exec_command(cmd)

    def send_cmd(self, cmd):
        # print("CMD to run in %s %s"%(self.ip, cmd))
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()  # Blocking call
        # if exit_status == 0:
        #     print("'%s' is complete"%cmd)
        # else:
        #     print("Error", exit_status)
        return stdout.read().decode('utf-8')