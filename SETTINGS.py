# KVM section
IMAGES_PATH = "/var/lib/libvirt/images/"
DEFAULT_VM_IMAGE_PATH = IMAGES_PATH + "carrier.qcow2"
BENCHMARK_PATH = "/home/odissey/disser/"
BASE_NET_XML = BENCHMARK_PATH + "base_net.xml"
BASE_VM_XML = BENCHMARK_PATH + "base_domain.xml"
USER = "root"
PASSWORD = "r00tme"

# Docker section
BASE_IMAGE = "daronar/base_phoronix"

#Docker in vm section
DOCKERINVM_IMAGE_PATH = IMAGES_PATH + "dockerinvm.qcow2"
DOCKERINVM_XML = BENCHMARK_PATH + "dockerinvm.xml"

CPU_NUM = 8
RAM_NUM = 7896*1024