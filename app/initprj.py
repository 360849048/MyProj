from multiprocessing import Process
from app import views
from app.dailytask import updatePathInfoAutomatically
from app import app


def start():
    p = Process(target=updatePathInfoAutomatically, args=())
    p.start()
    # 默认flask，包括debug模式，它是单线程后台
    # 当threaded=True时，采用多线程模式
    # app.run(host='127.0.0.1', port=8080, threaded=True)
    app.run(debug=True)
