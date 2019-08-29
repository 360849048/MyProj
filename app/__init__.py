from flask import Flask
import os

app = Flask(__name__)
# 如果使用了flask中的session，由于flask是将session加密后存储在客户端，
# 因此必须使用下面语句设置一个秘钥，将session加密后保存在cookie中。
# app.config['SECRET_KEY'] = os.urandom(24)
