# KVM section
IMAGES_PATH = "/var/lib/libvirt/images/"
DEFAULT_VM_IMAGE_PATH = IMAGES_PATH + "carrier.qcow2"
BASE_NET_XML = "/home/odissey/disser/base_net.xml"
BASE_VM_XML = "/home/odissey/disser/base_domain.xml"
USER = "root"
PASSWORD = "r00tme"

# Docker section
BASE_IMAGE = "daronar/base_phoronix"


CPU_NUM = 8
RAM_NUM = 4*1024*1024