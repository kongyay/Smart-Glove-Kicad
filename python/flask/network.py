import socket
import fcntl
import struct
import NetworkManager

class Network(object):
    def __init__(self):
            self.ip = ""

    def get_ip(self,ifname='wlan0'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24])
        self.ip = ip 
        return ip 
    
    def switch_ap(self,ap_on = true):
        if(ap_on):
            self.device

try:
    nw = Network()
    print(nw.ip)
    for d in NetworkManager.NetworkManager.GetDevices():
        print(d.Interface)
        if d.Interface == "wlan0":
            nw.device = d
            break

    print(nw.device.AvailableConnections[0].GetSettings()['connection'])
    # print(nw.device.AccessPoints[0].Ssid)
except OSError:
    print("Error Init NW")