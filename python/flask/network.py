import socket
import fcntl
import struct
import NetworkManager
import uuid

class Network(object):
    def __init__(self):
            self.ip = ""

    def get_ip(self,ifname='wlan0'):
        # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # ip = socket.inet_ntoa(fcntl.ioctl(
        #     s.fileno(),
        #     0x8915,  # SIOCGIFADDR
        #     struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        # )[20:24])
        ip = 'No IP Addr...'
        if self.device:
            addr = self.device.Ip4Config.Addresses
            if len(addr) > 0:
                ip = addr[0][0]
            # print(addr)

        self.ip = ip
        return ip 

    def get_cons(self):
        return list(map(lambda x: x.GetSettings()['connection']['id'], NetworkManager.Settings.ListConnections())) 
    
    def switch_con(self,name,pw):
        for con in NetworkManager.Settings.ListConnections():
            cn = con.GetSettings()['connection']['id']
            if cn == name:
                NetworkManager.NetworkManager.ActivateConnection(con, self.device, "/")
                return
        self.add_con(name,pw)


    def add_con(self,name,pw):
        new_connection = {
            '802-11-wireless': {    'mode': 'infrastructure',
                                    'security': '802-11-wireless-security',
                                    'ssid': name},
            '802-11-wireless-security': {   'key-mgmt': 'wpa-psk',
                                            'auth-alg': 'open',
                                            'psk': pw},
            'connection': { 'id': name,
                            'type': '802-11-wireless',
                            'uuid': str(uuid.uuid4())},
            'ipv4': {'method': 'auto'},
            'ipv6': {'method': 'auto'}
        }

        NetworkManager.Settings.AddConnection(new_connection)

try:
    nw = Network()
    for d in NetworkManager.NetworkManager.GetDevices():
        print(d.Interface)
        if d.Interface == "wlan0":
            nw.device = d
            break

    # print(nw.device.GetAppliedConnection(0).GetSettings())
    # print(nw.device.AccessPoints[0].Ssid)
except OSError:
    print("Error Init NW")