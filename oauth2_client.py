#coding: gbk
import base64
import random
import time
import json
import hmac
from datetime import datetime, timedelta

import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, request, redirect, make_response

app = Flask(__name__)

port='5001'
redirect_uri='http://localhost:'+port+'/client/passport'
client_id = '123456'







# �ͻ���
@app.route('/client/login', methods=['POST', 'GET'])
def client_login():
    uri = 'http://localhost:5000/oauth?response_type=code&client_id=%s&redirect_uri=%s' % (client_id, redirect_uri)
    return redirect(uri)

@app.route('/client/passport', methods=['POST', 'GET'])
def client_passport():
    code = request.args.get('code')
    uri = 'http://localhost:5000/oauth?grant_type=authorization_code&code=%s&redirect_uri=%s&client_id=%s' % (code, redirect_uri, client_id)
    #��code �� token��
    # try:
    #print "----2---"
    print "get code:"+code
    r = requests.get(uri)
    print "get token by code:"+r.text
    # except Exception,e:
    #     print e


    #��token �� userinfo
    uri='http://localhost:5000/test1?token=%s' % (r.text)
    r = requests.get(uri)
    print "get userInfo by token:" + r.text

    #save user info

    #��½��ƽ̨�ɹ��������û���½״̬�Ĳ�������session��cookie�ȱ����½��ƽ̨��״̬�����û�ȥ��ƽ̨��ҳ

    return unicode("��Ȩ�ɹ�����ƽ̨�Լ���������Ϣ��",'gbk')+r.text


@app.route('/test2', methods=['POST', 'GET'])
def test2():
    return 'hello2'



if __name__ == '__main__':
    app.run(port=int(port)) #flask �Դ��ķ��������� app