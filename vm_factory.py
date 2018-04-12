import libvirt
import SETTINGS
import subprocess
from bs4 import BeautifulSoup
import time
import mac_generator
from virtual_machine import virtual_machine
from Exceptions.vm_exception import VMException

class vm_factory:
    def __init__(self):
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

    def start_vm(self, vm: virtual_machine):
        domain = self.conn.defineXML(vm.xml)
        domain.create()
        return domain
        # init new VM class instance?


    def learn_ip_of_vm(self, vm: virtual_machine):
        tmp = self.conn.networkLookupByName("base-net")
        # tmp = self.conn.networkLookupByName("default")
        entries = tmp.DHCPLeases(mac=vm.mac)
        while len(entries) == 0:
            time.sleep(5)
            entries = tmp.DHCPLeases(mac=vm.mac)
        return entries[0]['ipaddr']


    def start_test_instance(self, test_name, install_cmd):
        vm = virtual_machine()
        if len(self.workers) == 0:
            vm.name = test_name + '0'
            # 1. Copy base image for new test
            self.clone_image(SETTINGS.DEFAULT_VM_IMAGE_PATH, SETTINGS.IMAGES_PATH + vm.name + ".qcow2")
            # 2. Create new xml
            vm.image = SETTINGS.IMAGES_PATH + vm.name + ".qcow2"
            vm.mac = self.mac_generator.randomMAC()
            vm.xml = self.update_xml(vm.name, SETTINGS.IMAGES_PATH + vm.name + ".qcow2", vm.mac)
            # 3. Start vm
            vm.domain = self.start_vm(vm)
            # 4. Wait booting
            time.sleep(5)
            # 5. Find IP
            vm.ip = self.learn_ip_of_vm(vm)
            print(vm.ip)
            # 6. Open SSH
            vm.open_ssh()
            # 7. Install test
            vm.send_cmd(install_cmd)
            # Machine is ready for image copying and testing
        else:
            vm.name = test_name + str(len(self.workers))
            # 1. Copy first image with test for new test
            self.clone_image(self.workers[0].image, SETTINGS.IMAGES_PATH + vm.name + ".qcow2")
            # 2. Create new xml
            vm.image = SETTINGS.IMAGES_PATH + vm.name + ".qcow2"
            vm.mac = self.mac_generator.randomMAC()
            vm.xml = self.update_xml(vm.name, SETTINGS.IMAGES_PATH + vm.name + ".qcow2", vm.mac)
            # 3. Start vm
            vm.domain = self.start_vm(vm)
            # 4. Wait booting
            time.sleep(5)
            # 5. Find IP
            vm.ip = self.learn_ip_of_vm(vm)
            print(vm.ip)
            # Machine is ready for image copying and testing
        self.workers.append(vm)
        return vm




    def clone_image(self, path_to_old, path_to_new):
        cur_time = time.time()
        cp = subprocess.Popen(["cp", path_to_old, path_to_new], stdout=subprocess.PIPE)
        cp.wait()
        print("CP END TIME", time.time() - cur_time)

    def update_xml(self, new_name, new_path, new_mac):
        print(new_name, new_path, new_mac)
        soup = BeautifulSoup(open(SETTINGS.BASE_VM_XML), "xml")
        # soup.findAll('name')[0] = new_name
        soup.find('name').contents[0].replaceWith(new_name)
        soup.findAll('source')[0]['file'] = new_path
        # TODO changehostname
        soup.findAll('mac')[0]['address'] = new_mac
        # print(soup)
        return str(soup)




vmf = vm_factory()
# vmf.start_test_vm("simple_test", "ifconfig")
vmf.start_test_instance("simple_test", "phoronix-test-suite install pts/john-the-ripper")
vmf.start_test_instance("simple_test", "phoronix-test-suite install pts/john-the-ripper")

# vmf.update_xml("hui", "/home/disser", "adad")
# vm = virtual_machine()
# vm.ip = "10.228.61.57"
# vm.open_ssh()
# vm.send_cmd('ifconfig')