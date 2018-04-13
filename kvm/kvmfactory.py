import libvirt
import SETTINGS
import subprocess
from bs4 import BeautifulSoup
import time
from helpers import mac_generator
from kvm.virtuamachine import VirtuaMachine
from helpers.cpu_controller import CPUController

class KvmFactory:
    def __init__(self, cpu_num=None, ram_num=None):
        self.cpu_con = CPUController()
        self.cpu_num = cpu_num
        self.ram_num = ram_num
        self.workers = []
        self.mac_generator = mac_generator.mac_generator()
        self.conn = libvirt.open("qemu:///system")
        #base network control
        try:
            self.net = self.conn.networkLookupByName("base-net")
        except libvirt.libvirtError:
            self.net = self.conn.networkDefineXML(open(SETTINGS.BASE_NET_XML).read())
            self.net.create()
            self.net.setAutostart(1)
        else:
            if not self.net.isActive():
                self.net.create()
                self.net.setAutostart(1)


    def start_vm(self, vm: VirtuaMachine):
        domain = self.conn.defineXML(vm.xml)
        domain.create()
        return domain
        # init new VM class instance?

    def destroy_vm(self, vm: VirtuaMachine):
        vm.ssh.close()
        vm.domain.destroy()
        vm.domain.undefine()
        self.remove_image(vm.image)


    def destroy(self):
        for vm in self.workers:
            self.destroy_vm(vm)
        self.conn.close()
        self.workers = []

    def learn_ip_of_vm(self, vm: VirtuaMachine):
        tmp = self.conn.networkLookupByName("base-net")
        # tmp = self.conn.networkLookupByName("default")
        entries = tmp.DHCPLeases(mac=vm.mac)
        while len(entries) == 0:
            time.sleep(5)
            entries = tmp.DHCPLeases(mac=vm.mac)
        return entries[0]['ipaddr']


    def start_test_carrier(self, test_name, install_cmd):
        vm = VirtuaMachine()
        if len(self.workers) == 0:
            vm.name = test_name + '0'
            print("# 1. Copy base image for new test")
            self.clone_image(SETTINGS.DEFAULT_VM_IMAGE_PATH, SETTINGS.IMAGES_PATH + vm.name + ".qcow2")
            print("# 2. Create new xml")
            vm.image = SETTINGS.IMAGES_PATH + vm.name + ".qcow2"
            vm.mac = self.mac_generator.randomMAC()
            vm.xml = self.update_xml(vm.name, SETTINGS.IMAGES_PATH + vm.name + ".qcow2", vm.mac)
            print("# 3. Start vm")
            vm.domain = self.start_vm(vm)
            print("# 4. Wait booting")
            time.sleep(10)
            print("# 5. Find IP")
            vm.ip = self.learn_ip_of_vm(vm)
            print(vm.ip)
            print("# 6. Open SSH")
            vm.open_ssh()
            print("# 7. Install test_organisation and wait its' finishing")
            vm.send_cmd(install_cmd)
            # Machine is ready for image copying and testing
        else:
            vm.name = test_name + str(len(self.workers))
            print("# 1. Copy first image with test_organisation for new test")
            self.clone_image(self.workers[0].image, SETTINGS.IMAGES_PATH + vm.name + ".qcow2")
            print("# 2. Create new xml")
            vm.image = SETTINGS.IMAGES_PATH + vm.name + ".qcow2"
            vm.mac = self.mac_generator.randomMAC()
            vm.xml = self.update_xml(vm.name, SETTINGS.IMAGES_PATH + vm.name + ".qcow2", vm.mac)
            print("# 3. Start vm")
            vm.domain = self.start_vm(vm)
            print("# 4. Wait booting")
            time.sleep(5)
            print("# 5. Find IP")
            vm.ip = self.learn_ip_of_vm(vm)
            print(vm.ip)
            print("# 6. Open SSH")
            vm.open_ssh()
        self.workers.append(vm)
        return vm


    def remove_image(self, path):
        rm = subprocess.Popen(["rm", path], stdout=subprocess.PIPE)

    def clone_image(self, path_to_old, path_to_new):
        cur_time = time.time()
        cp = subprocess.Popen(["cp", path_to_old, path_to_new], stdout=subprocess.PIPE)
        cp.wait()
        print("CP END TIME", time.time() - cur_time)

    def update_xml(self, new_name, new_path, new_mac):
        # print(new_name, new_path, new_mac)
        soup = BeautifulSoup(open(SETTINGS.BASE_VM_XML), "xml")
        # soup.findAll('name')[0] = new_name
        soup.find('name').contents[0].replaceWith(new_name)
        soup.findAll('source')[0]['file'] = new_path

        if self.cpu_num is not None:
            soup.find('vcpu')['cpuset'] = self.cpu_con.get_new_set(self.cpu_num)

        if self.cpu_num is None:
            soup.find('vcpu').contents[0].replaceWith(str(SETTINGS.CPU_NUM))
        else:
            soup.find('vcpu').contents[0].replaceWith(str(self.cpu_num))

        if self.ram_num is None:
            soup.find('memory').contents[0].replaceWith(str(SETTINGS.RAM_NUM))
        else:
            soup.find('memory').contents[0].replaceWith(str(self.ram_num))

        soup.findAll('mac')[0]['address'] = new_mac
        # print(soup)
        return str(soup)



if __name__ == "__main__":
    vmf = KvmFactory()
    vmf.update_xml("hui", "/home/disser", "adad")

# vmf.start_test_vm("simple_test", "ifconfig")
#     vmf.start_test_carrier("simple_test", "phoronix-test_organisation-suite install pts/john-the-ripper")
    # vmf.start_test_instance("simple_test", "phoronix-test_organisation-suite install pts/john-the-ripper")
#
# # vmf.update_xml("hui", "/home/disser", "adad")
# # vm = virtual_machine()
# # vm.ip = "10.228.61.57"
# # vm.open_ssh()
# # vm.send_cmd('ifconfig')