import socket
import sys
import time
import json


def create_socket(port, local_ip = '', multicast_ip=''):
    """ Create a UDP listening socket
        Supports both UDP unicast and multicast
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((multicast_ip, port))

    if multicast_ip:
        mreq = struct.pack("4sl", socket.inet_aton(multicast_ip), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    return sock


def start_sending():
    """ Start UDP client """

    local_ip = '0.0.0.0'
    sock = create_socket(0, local_ip)

    #remote_ip = '10.40.9.145'
    #remote_ip = '10.40.7.196'
    remote_ip = '192.168.43.193'
    remote_port = 9000

    t0 = time.time()
    channels = ['tv1', 'tv2']
    index = 0

    while True:
        try:
            obj = {'type': 'channel_change', 'channel': channels[index]}
            sent = sock.sendto(json.dumps(obj), (remote_ip, remote_port))
            print 'sent data:', sent, json.dumps(obj)
        except Exception as e:
            print e

        #sent = sock.sendto(response, addr)
        #print 'sent %s bytes' % sent

        t1 = time.time()
        if t1 - t0 > 10:
            index = index + 1
            if index >= len(channels):
                index = 0
            t0 = t1

        time.sleep(1)


if __name__ == '__main__':
    start_sending()

