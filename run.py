from app import app

# 该后台是单线程服务，暂时无需担心数据库并发写入情况锁死数据库情况
# app.run(host='172.18.71.158', port=8080, threaded=True)
app.run(debug=True)
