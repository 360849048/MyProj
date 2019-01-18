if __name__ == '__main__':
    from multiprocessing import Process
    from app import app
    from app.dailytask import updatePathInfoAutomatically
    from app.pathinfo import *
    from app.sqljob import DbManager

    # # 新增版本路径标记功能，为了兼容数据库，每个表需要加入新字段
    # db_soft = DbManager(SOFTWARE_VERSION_INFO_DB_PATH)
    # for table_name in db_soft.getAllTables():
    #     if table_name == 'sqlite_sequence':
    #         continue
    #     db_soft.addTableColumns(table_name, 'torefresh')

    p = Process(target=updatePathInfoAutomatically, args=())
    p.start()
    # 默认flask，包括debug模式，它是单线程后台
    # 当threaded=True时，采用多线程模式
    app.run(host='127.0.0.1', port=8080, threaded=True)
    # app.run(debug=True)
