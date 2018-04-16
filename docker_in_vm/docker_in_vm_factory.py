from container.dockercontainer import DockerContainer
import SETTINGS
from container.docker_factory import DockerFactory
import libvirt
from bs4 import BeautifulSoup
import docker
import time

class DockerInVmFactory(DockerFactory):
    def __init__(self, cpu_num=None, ram_num=None):
        super().__init__(cpu_num, ram_num)
        self.kvm_conn = libvirt.open("qemu:///system")
        soup = BeautifulSoup(open(SETTINGS.DOCKERINVM_XML), "xml")
        soup.findAll('source')[0]['file'] = SETTINGS.DOCKERINVM_IMAGE_PATH
        soup.find('vcpu').contents[0].replaceWith(str(SETTINGS.CPU_NUM))
        soup.find('memory').contents[0].replaceWith(str(SETTINGS.RAM_NUM))
        self.dockerinvm = self.kvm_conn.defineXML(str(soup))
        self.dockerinvm.create()

        default_net = self.kvm_conn.networkLookupByName("default")
        entries = default_net.DHCPLeases()
        ip = ""
        for i in entries:
            if i["hostname"] == "dockerinvm":
                ip = i["ipaddr"]
                break

        time.sleep(30)
        self.conn = docker.DockerClient(base_url="tcp://" + ip + ":2375")
        # self.conn = docker.DockerClient(base_url="tcp://192.168.122.238:2375")

        # print(self.conn.images.list())

    def destroy(self):
        super().destroy()
        self.dockerinvm.destroy()
        self.dockerinvm.undefine()



if __name__ == "__main__":
    dvm = DockerInVmFactory()
