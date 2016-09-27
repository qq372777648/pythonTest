# coding:gbk
from flask import Flask, request, url_for, render_template, flash,abort
from models import User
import  time
from functools import wraps
from flask import make_response
import json
import  logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='i://myapp.log',
                filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)




app = Flask(__name__) #传name flask 就知道当前脚本所在路径
app.secret_key = '123' # use flask msg must set a secretkey


#每次返回数据中，带上响应头，包含API版本和本次请求的requestId，以及允许所有域跨域访问API, 记录访问日志

def afterLog(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):


        ret=fun(*args, **kwargs)
        response = make_response(ret)
        print "log"


        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,PUT,GET,POST,DELETE'
        response.headers['Access-Control-Allow-Headers'] = "Referer,Accept,Origin,User-Agent"
        logging.info(json.dumps({
                "AccessLog": {
                "status_code": response.status_code,
                "method": request.method,
                "ip": request.headers.get('X-Real-Ip', request.remote_addr),
                "url": request.url,
                "referer": request.headers.get('Referer'),
                "agent": request.headers.get("User-Agent"),
                    "heh":"11111111"
                }
            }))
        return response
    return wrapper_fun







@app.route('/delay')
def delay():
    time.sleep(5)
    return 'delay happiness'

@app.route('/')
@afterLog
def hello_world():
    print "hello world"
    return 'xxxHello World!'


@app.route('/user/<id>', methods=['POST', "get"])
def hello_user(id):
    pw= request.args.get('pw')
    return 'xhello user:' + id +" pw:"+pw


@app.route('/getUser')
def get_user():
    return '1'

@app.route('/getUrl') #根据函数名查路由
def query_url():
    return 'query url:'+url_for('get_user')

@app.route('/user/info/<id>')
def user_index(id):
    user =None
    if int(id) == 1:
        user =User(1, 'lzw', 23)
    return render_template("one_base.html", user=user , msg="xxxxxxxxx")

@app.route('/user/list')
def user_list():
    users = []
    for i in range(1,11):
        user = User(i, unicode("中午",'gbk'), 20)  #unicode("中午",'gbk')
        users.append(user)
    return render_template("two_base.html",users=users)

@app.route("/toLogin")
def to_login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    form = request.form
    username = form.get('username')
    password = form.get('password')

    if not username:
        flash("please input username")
        return render_template("login.html")
    if not password:
        flash("please input password")
        return render_template("login.html")

    if username == '1' and password == '1':
        flash("login success")
        abort(404)
    else:
        flash("username or password is wrong")
        return render_template("login.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")




if __name__ == '__main__':
    app.run(port=9004)