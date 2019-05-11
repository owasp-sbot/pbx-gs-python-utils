import socket
import ssl
from   urllib.request import Request, urlopen
#import websocket


def DELETE(url, data='', headers={}):
    return Http_Request(url, data, headers, 'DELETE')


def GET(url,headers = {}, encoding = 'utf-8'):
    return Http_Request(url, data='', headers=headers, method='GET', encoding=encoding)


def POST(url, data='', headers={}):
    return Http_Request(url, data, headers, 'POST')


def PUT(url, data='', headers={}):
    return Http_Request(url, data, headers, 'PUT')


def Http_Request(url, data='', headers={}, method='POST', encoding = 'utf-8' ):
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    request  = Request(url, data.encode(), headers=headers)
    request.get_method = lambda: method
    return urlopen(request, context=gcontext).read().decode(encoding)


def WS_is_open(ws_url):
    try:
        import websocket                 # was causing issues in lambda (couldn't find it)
        ws = websocket.WebSocket()
        ws.connect(ws_url)
        return ws.connected
    except:
        return False


def port_is_open(port, host='0.0.0.0'):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    return result == 0


def current_host_online():
    try:
        Http_Request('http://www.google.com', method='HEAD')
        return True
    except:
        return False


# code below is not reliable enough (was trying to get the time from an ntp server, but it hanged a couple times during tests)
# note: this could had been caused by VPN issues (I was having at the time with the Cisco VPN client)
# def gettime_ntp(self, ntp_server='0.uk.pool.ntp.org'):
#     #ntp_server = 'europe.pool.ntp.org'
#     # based on http://code.activestate.com/recipes/117211-simple-very-sntp-client/
#     import struct
#     import sys
#     import time
#
#     TIME1970 = 2208988800  # Thanks to F.Lundh
#
#     from _socket import AF_INET
#     from _socket import SOCK_DGRAM
#     from socket import socket
#     client = socket(AF_INET, SOCK_DGRAM)
#     data = '\x1b' + 47 * '\0'
#     client.sendto(data.encode(), (ntp_server, 123))
#     client.settimeout(2)
#     data, address = client.recvfrom(1024)
#     if data:
#         print('Response received from:', address)
#         t = struct.unpack('!12I', data)[10]
#         t -= TIME1970
#         date = time.ctime(t)
#
#
#         when = strftime("%Y/%m/%d %H:%M", localtime(t))
#         print(when)
#         print('\tTime=%s' % time.ctime(t))