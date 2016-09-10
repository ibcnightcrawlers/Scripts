import socket
import sys
import time
import json


def create_listening_socket(port, local_ip = '', multicast_ip=''):
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


def start_listen(ip, port):
    """ Start UDP server """

    #local_ip = '10.40.9.145'
    local_ip = '0.0.0.0'
    sock = create_listening_socket(port, local_ip)

    print 'Listening for data'
    t0 = time.time()

    while True:
        data, addr = sock.recvfrom(1500)
        print 'got data:', data, 'from:', addr

        t1 = time.time()
        if t1 - t0 > 10:
            response = {"type": "offer"}
            t0 = t1
            print 'offer request'
        else:
            response = {"type": "ok"}

        sent = sock.sendto(json.dumps(response), addr)
        print 'sent %s bytes' % sent


if __name__ == '__main__':
    start_listen('0.0.0.0', int(sys.argv[1]))

