import random

class mac_generator:
    def __init__(self):
        self.used_macs = []

    def randomMAC(self):
        return self.MACprettyprint([ 0x00, 0x00, 0x00,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ])

    def MACprettyprint(self, mac):
        pretty_mac = ':'.join(map(lambda x: "%02x" % x, mac))
        while pretty_mac in self.used_macs:
            pretty_mac = ':'.join(map(lambda x: "%02x" % x, mac))
        self.used_macs.append(pretty_mac)
        return pretty_mac
