import ssl
from urllib.request import Request, urlopen

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