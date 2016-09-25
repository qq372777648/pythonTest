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







# 客户端
@app.route('/client/login', methods=['POST', 'GET'])
def client_login():
    uri = 'http://localhost:5000/oauth?response_type=code&client_id=%s&redirect_uri=%s' % (client_id, redirect_uri)
    return redirect(uri)

@app.route('/client/passport', methods=['POST', 'GET'])
def client_passport():
    code = request.args.get('code')
    uri = 'http://localhost:5000/oauth?grant_type=authorization_code&code=%s&redirect_uri=%s&client_id=%s' % (code, redirect_uri, client_id)
    #用code 拿 token，
    # try:
    #print "----2---"
    print "get code:"+code
    r = requests.get(uri)
    print "get token by code:"+r.text
    # except Exception,e:
    #     print e


    #用token 拿 userinfo
    uri='http://localhost:5000/test1?token=%s' % (r.text)
    r = requests.get(uri)
    print "get userInfo by token:" + r.text

    #save user info

    #登陆本平台成功，进行用户登陆状态的操作（如session、cookie等保存登陆本平台的状态，让用户去本平台主页

    return unicode("授权成功！本平台以及获得你的信息：",'gbk')+r.text


@app.route('/test2', methods=['POST', 'GET'])
def test2():
    return 'hello2'



if __name__ == '__main__':
    app.run(port=int(port)) #flask 自带的服务器启动 app