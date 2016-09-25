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

users = {
    "lzw": ["123"]
}

port='5000'
redirect_uri='http://localhost:'+port+'/client/passport'
client_id = '123456'
users[client_id] = []
auth_code = {}

oauth_redirect_uri = []

TIMEOUT = 3600 * 2


# �°汾��token������
def gen_token(data):
    '''
    :param data: dict type
    :return: base64 str
    '''
    data = data.copy()
    if "salt" not in data:
        data["salt"] = unicode(random.random()).decode("ascii")
    if "expires" not in data:
        data["expires"] = time.time() + TIMEOUT
    payload = json.dumps(data).encode("utf8")
    # ����ǩ��
    sig = _get_signature(payload)
    return encode_token_bytes(payload + sig)

# ��Ȩ��������
def gen_auth_code(uri, user_id):
    code = random.randint(0,10000)
    auth_code[code] = [uri, user_id]
    return code

# �°汾��token��֤
def verify_token(token):
    '''
    :param token: base64 str
    :return: dict type
    '''
    decoded_token = decode_token_bytes(str(token))
    payload = decoded_token[:-16]
    sig = decoded_token[-16:]
    # ����ǩ��
    expected_sig = _get_signature(payload)
    if sig != expected_sig:
        return {}
    data = json.loads(payload.decode("utf8"))
    if data.get('expires') >= time.time():
        return data
    return 0

# ʹ��hmacΪ��Ϣ����ǩ��
def _get_signature(value):
    """Calculate the HMAC signature for the given value."""
    return hmac.new('secret123456', value).digest()

# ��������������base64����ͽ��뵥����װ
def encode_token_bytes(data):
    return base64.urlsafe_b64encode(data)

def decode_token_bytes(data):
    return base64.urlsafe_b64decode(data)


# ��֤��������

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     uid, pw = base64.b64decode(request.headers['Authorization'].split(' ')[-1]).split(':')
#     if users.get(uid)[0] == pw:
#         return gen_token(dict(user=uid, pw=pw))
#     else:
#         return 'error'

#user login- user grant- server send code to fristParty- fristParty get token by code - server send token to fristParty -  fristPartyget userInfo by token
@app.route('/oauth', methods=['POST', 'GET'])
def oauth():
    # �������¼�� ͬʱ����Cookie
    if request.method == 'POST' and request.form['user']:
        u = request.form['user']
        p = request.form['pw']
        if users.get(u)[0] == p and oauth_redirect_uri:
            # �˴�����׼Ӧ����ѯ���û��Ƿ���Ȩ
            uri = oauth_redirect_uri[0] + '?code=%s' % gen_auth_code(oauth_redirect_uri[0], u)  #����д����0����ʵ��Ӧ��ͨ��һ���㷨���ڴ����ҵ��ض����ַ  request.args.get('redirect_uri')+...
            expire_date = datetime.now() + timedelta(minutes=1)
            resp = make_response(redirect(uri))
            resp.set_cookie('login', '_'.join([u, p]), expires=expire_date)
            return resp #����Ȩ�롢��½cookie���ض��򵽵�����

    # ��֤��Ȩ�룬����token (����������)
    if request.args.get('code'):
        auth_info = auth_code.get(int(request.args.get('code')))
        if auth_info[0] == request.args.get('redirect_uri'): #����ѧ��Ӧ�ñȶ���ʵ������url
            # ��������Ȩ���auth_code�д洢�û��������token��
            return gen_token(dict(client_id=request.args.get('client_id'), user_id=auth_info[1]))


    # �����¼�û���Cookie����ֱ����֤�ɹ���������Ҫ��д��¼��
    if request.args.get('redirect_uri'):
        oauth_redirect_uri.append(request.args.get('redirect_uri'))
        if request.cookies.get('login'):#��cookie
            u, p = request.cookies.get('login').split('_')
            if users.get(u)[0] == p:
                uri = oauth_redirect_uri[0] + '?code=%s' % gen_auth_code(oauth_redirect_uri[0], u)
                return redirect(uri)
        return '''
            <form action="" method="post">
                <p><input type=text name=user>
                <p><input type=text name=pw>
                <p><input type=submit value=Login>
            </form>
        '''

# ��Դ��������
@app.route('/test1', methods=['POST', 'GET'])
def test():
    token = request.args.get('token')
    ret = verify_token(token) #Ӧ�ø��ݹؼ�������������ǩ�� ��token�ȶ�
    if ret:
        return json.dumps(ret)
    else:
        return 'error'



if __name__ == '__main__':
    # from werkzeug.contrib.fixers import ProxyFix
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    #gunicorn hello:app
    app.run(port=int(port)) #flask �Դ��ķ��������� app