#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import os
import socket
import time
from pprint import pformat

from bottle import route, template, run, request, response, post, static_file

BOTTLE_STATIC_DIR = '/home/kossmak/proj/bottle-cork/static'
# TIMEOUT = 62
TIMEOUT = 60

# socket.setdefaulttimeout(TIMEOUT)


@route('/bottle/try_out', method='ANY')
def try_out():
    response.content_type = 'text/html'
    return u'''\
<html>
<title>Bottle-cork is opened</title>
  <body>
    <div><b>OK</b></div>
    <div>utc: {dt}</div>
  </body>
</html>
'''.format(dt=datetime.datetime.utcnow())

@route('/bottle/bad_soap', method='ANY')
def bad_soap():
    # response.headers['Content-Type'] = 'xml/application'
    response.content_type = 'xml/application'
    response.status = 403
    return u'''\
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <doc>
    <tag code="RUB">111</tag>
    <tag code="RUB">222</tag>
  </doc>
</soap:Envelope>
'''


@post('/bottle/crt/reserve')
def index(**kw):
    print "\n---------"
    print "request: ", request.body.read()
    print "cookie: ", pformat(request.cookies)
    response.content_type = 'application/json'
    result = {
        "data": {
            "reservationId": "FUPG891351"
        },
        "errors": [],
        "isSuccess": True
    }
    return json.dumps(result)


@post('/bottle/svc/error_rs')
def index_error_rs(**kw):
    print "\n---------"
    print "request: ", request.body.read()
    print "cookie: ", pformat(request.cookies)
    response.content_type = 'application/json'
    result = u'''\
{
    "isSuccess": false,
    "errors": [
        {
            "message": "Не было найдено ваучеров по входящим параметрам",
            "code": "1001000333",
            "dbg": "SiebelNoCertificatesFound",
            "value": null
        }
    ],
    "data": null
}
    '''
    return result
    # return result.encode('utf-8')


@route('/bottle/static/<filepath:path>')
def server_static(filepath):
    time.sleep(1)
    # time.sleep(TIMEOUT-50)
    return static_file(filepath, root=BOTTLE_STATIC_DIR)


@route('/bottle/upload', method='POST')
def do_upload(**kw):

    # FIXME: [debug] remove
    # time.sleep(5)  

    # category = request.forms.get('category')
    saved_paths = []
    if not request.files:
        raise ValueError('Bad request format. No files.')
    for param_name in request.files:
        # upload = request.files.get('upload')
        uploaded_file = request.files.get(param_name)
        if not uploaded_file:
            continue
        name, ext = os.path.splitext(uploaded_file.filename)
        # if ext not in ('.png', '.jpg', '.jpeg'):
        #     return "File extension not allowed."

        # save_path = "/tmp/{category}".format(category=category)
        # save_path = '/tmp/{}{}'.format(name, ext)
        save_path = os.path.join(os.path.dirname(__file__), 'static', 'incoming')
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        # file_path = os.path.join(save_path, upload.filename)
        file_path = os.path.join(save_path, uploaded_file.raw_filename)

        if os.path.isfile(file_path):
            # raise ReferenceError('File {} already uploaded'.format(file_path))
            print '{} exists, removing...'.format(file_path)
            os.unlink(file_path)
            print '{} removed'.format(file_path)

        uploaded_file.save(file_path)
        # or for old bottle's versions:
        # with open(file_path, 'wb') as open_file:
        #     open_file.write(upload.file.read())
        saved_paths.append(file_path)

    return "Files successfully saved to \n'{0}'\n".format(pformat(saved_paths))


# run(host='localhost', port=8880)
run(host='0.0.0.0', port=8880)

