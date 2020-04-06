from flask import request, send_file, jsonify, make_response, session
import hmac
from app import app
from app.pathinfo import *
from app.log2 import log
from app.pwd5 import createPwd5
import app.user as user
from app import ioviews
from app import vertionviews
from app import SECRET_KEY_NORMAL
from app import SECRET_KEY_ADMIN


@app.route('/', methods=['GET', 'POST'])
def home():
    resp = make_response(send_file(ENTRY_HTML_PATH))
    resp.headers['Cache-Control'] = "no-cache"
    return resp
    # return send_file(ENTRY_HTML_PATH)

# 没有下面404处理，会导致vue-router在history模式下一刷新就404错误
@app.errorhandler(404)
def pageNotFound(e):
    resp = make_response(send_file(ENTRY_HTML_PATH))
    resp.headers['Cache-Control'] = "max-age=0"
    return resp
    # return send_file(ENTRY_HTML_PATH)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    client_ip = request.remote_addr
    account = data["account"]
    pwd = data["pwd"]

    verfiy_status = user.verifyAccount(account, pwd)

    if verfiy_status["status"]:
        response = make_response(jsonify({'status': 'success', 'username': verfiy_status['username'], 'sp': verfiy_status['admin']}))
        # 设置cookie
        response.set_cookie('account', account, httponly=True)
        if verfiy_status['admin']:
            response.set_cookie('sp', '1', httponly=True)
            h = hmac.new(SECRET_KEY_ADMIN, account.encode(), digestmod='MD5')
            response.set_cookie('ssid', h.hexdigest(), httponly=True)
        else:
            response.set_cookie('sp', '0', httponly=True)
            h = hmac.new(SECRET_KEY_NORMAL, account.encode(), digestmod='MD5')
            response.set_cookie('ssid', h.hexdigest(), httponly=True)
        # # 设置session
        # session['username'] = data['username']
        # session['access_level'] = 5
        # # 设置session过期时间，默认一个月有效
        # session.permanent = True
        log.record(ip=client_ip, event="登录", description="", username=account)

    else:
        response = make_response(jsonify({'status': 'failure', 'username': '', 'sp': False}))
        response.delete_cookie('account')
        response.delete_cookie('sp')
        response.delete_cookie('ssid')
        # # 设置session
        # session['user_ip'] = 0
        # # 读取seesion
        # user_level = session.get('user_ip')
        # print(user_level)
        # 删除session
        # session.pop('user_ip')

    return response

@app.route('/api/logout', methods=['GET'])
def logout():
    response = make_response()
    response.delete_cookie('account')
    response.delete_cookie('sp')
    response.delete_cookie('ssid')
    return response

@app.route('/api/verifystatus', methods=['GET'])
def verifyStatus():
    ret_data = {'status': False, 'username': '', 'sp': False, 'account': ''}
    account = request.cookies.get('account')
    sp = request.cookies.get('sp')
    ssid = request.cookies.get('ssid')

    if user.verifyCookies(account, sp, ssid):
        ret_data['status'] = True
        if sp == '1':
            ret_data['sp'] = True
        ret_data['account'] = account
        ret_data['username'] = user.verifyAccount(account, '')['username']

    return jsonify(ret_data)

@app.route('/api/modifypwd', methods=['POST'])
def modifyPwd():
    account = request.cookies.get('account')
    data = request.get_json()
    originPwd = data['originPwd']
    newPwd = data['newPwd']
    verfiy_status = user.verifyAccount(account, originPwd)
    ret_data = {'status': False, 'description': ''}
    if verfiy_status['status']:
        ret_data['status'] = user.modifyPwd(account, newPwd)
        if not ret_data['status']:
            ret_data['description'] = '后台处理失败，详细错误请见系统日志'
        else:
            ret_data['description'] = '密码修改成功'
            client_ip = request.remote_addr
            log.record(ip=client_ip, event="修改密码", description="", username=account)
    else:
        ret_data['description'] = '旧密码输入有误'
    return jsonify(ret_data)

@app.route('/api/modifyusername', methods=['GET'])
def modifyUsername():
    ret_data = {'status': False, 'description': ''}
    # 需要首先校验用户，防止cookie伪造
    account = request.cookies.get('account')
    sp = request.cookies.get('sp')
    ssid = request.cookies.get('ssid')
    if not user.verifyCookies(account, sp, ssid):
        ret_data['description'] = "请刷新页面或者重新登录后再重试！"
        return jsonify(ret_data)

    new_username = request.args.get('newUsername')
    ret_data['status'] = user.modifyUsername(account, new_username)
    if ret_data['status']:
        ret_data['description'] = '用户名修改成功！'
        client_ip = request.remote_addr
        log.record(ip=client_ip, event="修改用户名", description="新用户名：" + new_username, username=account)
    else:
        ret_data['description'] = '用户名修改失败，详情请见系统日志'
    return jsonify(ret_data)

@app.route('/api/log/userall', methods=['GET'])
def getUserLog():
    ret_data = {'status': False, 'list': ''}
    account = request.cookies.get('account')
    sp = request.cookies.get('sp')
    ssid = request.cookies.get('ssid')
    if user.verifyCookies(account, sp, ssid) and sp == '1':
        ret_data['status'] = True
        list_all = log.readAll()
        ret_data['list'] = list_all
    return jsonify(ret_data)

@app.route('/api/foo', methods=['GET', 'POST'])
def cookieTest():
    print('request.data: ', request.data)
    print('request.get_data(): ', request.get_data())
    print('request.form: ', request.form)
    print(request.form.get('username'))
    print(request.form.get('not_existed'))
    print(type(jsonify([1, 2, 3])))
    response = make_response(jsonify([1, 2, 3, 4]))
    print('request.cookies: ', request.cookies)
    print('session:', session.get('username'), session.get('access_level'))
    client_ip = request.remote_addr
    if session.get('user_ip') == client_ip:
        print('ip验证成功')
    return response

# ##################################### Others #################################
@app.route('/api/getpwd5', methods=['GET'])
def getPwd5():
    random_codes = request.args.get('randomcodes')
    return jsonify(createPwd5(random_codes))

@app.route('/api/srctransfer', methods=['POST'])
def getFile():
    files = request.files.getlist("file")
    print(files)
    for file in files:
        if file.filename != "":
            file.save("./app/static/cache/" + file.filename)
    return jsonify("ok")
