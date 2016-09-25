# coding:gbk
from flask import Flask, request, url_for, render_template, flash,abort
from models import User

app = Flask(__name__) #传name flask 就知道当前脚本所在路径
app.secret_key = '123' # use flask msg must set a secretkey



@app.route('/')
def hello_world():
    return 'xxHello World!'


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