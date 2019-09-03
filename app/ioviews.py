from flask import request, send_file, jsonify, make_response, session
import time
import shutil
from app import app
from app.sqljob import TableManager
from app.iomaker import IOMaker
from app.configfile import HkFileMaker, FcfFileMaker, SysFileMaker, SafetyFileMaker, createZip
from app.pathinfo import *
from app.log2 import log


@app.route('/api/io/iolist', methods=['GET'])
def getIo():
    io_type = request.args.get('type')
    start_id = int(request.args.get('start'))
    end_id = int(request.args.get('end'))
    # io_type可以是'DI', 'DO', 'AI', 'AO', 'TI', 'TO'
    if io_type == 'DI':
        t_io = TableManager('digital_input', IO_INFO_DB_PATH)
    elif io_type == 'DO':
        t_io = TableManager('digital_output', IO_INFO_DB_PATH)
    elif io_type == 'AI':
        t_io = TableManager('analog_input', IO_INFO_DB_PATH)
    elif io_type == 'AO':
        t_io = TableManager('analog_output', IO_INFO_DB_PATH)
    elif io_type == 'TI':
        t_io = TableManager('temperature_input', IO_INFO_DB_PATH)
    else:
        t_io = TableManager('temperature_output', IO_INFO_DB_PATH)
    ret_data = {}
    ret_data['amount'] = IOS_AMOUNT[io_type]
    ret_data['ios'] = {}
    if start_id > end_id or start_id > ret_data['amount']:
        return jsonify(ret_data)
    if end_id > ret_data['amount']:
        end_id = ret_data['amount']
    for id in range(start_id, end_id + 1):
        ret_data['ios'][str(id)] = t_io.displayBriefData(id, 'CName')[0]

    return jsonify(ret_data)

@app.route('/api/io/bigstdmodule', methods=['GET'])
def getBigIo():
    # 获取大机选配CIO021或CIO011的IO点配置信息
    # 数据返回格式为{'name': 'CIO021(或CIO011)', ios: {'di3': '83--开门', ..., 'do2': '113--润滑马达2'}}
    cio021_io = {
        'DI3': 83,
        'DI4': 84,
        'DI5': 85,
        'DI6': 97,
        'DI7': 98,
        'DI8': 99,
        'DO1': 97,
        'DO2': 98,
        'DO3': 113
    }
    if request.args.get('type').upper() == 'VE2':
        ret_data = {'name': 'CIO011', 'ios': {}}
    else:
        ret_data = {'name': 'CIO021', 'ios': {}}
    # t_di = TableManager('digital_input', IO_INFO_DB_PATH)
    # t_do = TableManager('digital_output', IO_INFO_DB_PATH)
    for k, v in cio021_io.items():
        if k.startswith('DI'):
            ret_data['ios'][k] = str(v)  # + '--' + t_di.displayBriefData(v, 'CName')[0]
        if k.startswith('DO'):
            ret_data['ios'][k] = str(v)  # + '--' + t_do.displayBriefData(v, 'CName')[0]
    return jsonify(ret_data)

@app.route('/api/io/pilzlist', methods=['GET'])
def getPilzList():
    ret_data = {'normal': [], 'e73': []}
    for file_name in os.listdir(NOR_SAFETY_RELAY_FILE_DIR):
        ret_data['normal'].append(file_name)
    for file_name in os.listdir(E73_SAFETY_RELAY_FILE_DIR):
        ret_data['e73'].append(file_name)

    ret_data['normal'].append('其他')
    ret_data['e73'].append('其他')
    return jsonify(ret_data)

@app.route('/api/io/funcoutlist', methods=['GET'])
def getOutputItems():
    t_func_list = TableManager('FuncOutput_List', IO_INFO_DB_PATH)
    ret_data = []
    for each_id in t_func_list.getAllId():
        ret_data.append(t_func_list.displayBriefData(each_id, 'CName')[0])
    return jsonify(ret_data)

@app.route('/api/io/createxlxs', methods=['POST'])
def createIoFile():
    '''
        生成IO表文件(.xlsx)
        目前后台只支持主底板和扩展底板一的编辑
        根据网页POST数据格式，进行数据处理。
        必须严格参照网页传输的数据进行编程
        * 2019.06.13: （Bug fix）当计算得到两份重名文件时，由于浏览器缓存原因，将下载得到两份一样的文件
    '''
    # data是一个dict对象
    data = request.get_json()
    client_ip = request.remote_addr
    record_info = 'IP: ' + client_ip + '创建IO表：\n'
    record_info += request.data.decode()
    log.record(ip=client_ip, event="创建IO表", description=request.data.decode(), username="")

    # 将post得到的数据整理成规范格式的数据
    board_1_modules_ios = []
    board_1 = data['boardModules1']
    board_1_ios = data['boardModulesIOs1']
    for idx in range(len(board_1)):
        if board_1[idx] != '':
            board_1_modules_ios.append([board_1[idx], board_1_ios[idx]])

    board_2_modules_ios = []
    board_2 = data['boardModules2']
    board_2_ios = data['boardModulesIOs2']
    for idx in range(len(board_2)):
        if board_2[idx] != '':
            board_2_modules_ios.append([board_2[idx], board_2_ios[idx]])

    evaluation_num = data['evaluationNum']
    production_num = data['productionNum']
    type_string = data['immType']
    customer = data['customer']
    safety_standard = data['safetyStandard']
    technical_clause = data['technicalClause']
    dual_inj = data['isDualInj']
    clamp_force = data['clampForce']
    injection = data['injection']
    # 这个是改造后规范显示的immType字符串，json中的immType值不适合取文件名
    imm_type = ''
    # 默认的主底板IO是否修改
    func_output1 = data['funcOutput1']
    func_output2 = data['funcOutput2']
    e73_safety = data['funcConfig']['3']['status']
    main_board_modified_io = data['mainBoardModifiedIo']
    # 能耗模块DEE是否启用
    energy_dee = data['funcConfig']['5']['status']
    # 功能点为是否更改为可编程输出
    # Varan连接模块如果启用，安装在KEB之后(0)之前(1)
    varan_conn_module_pos = data['varanConnModulePos']
    # 外置热流道是否激活，及组数
    # 注意网页端提交的功能序号可能随功能增加而改变，注意 data['funcConfig']['?']['status]中的序号('?')需要随之更新
    activate_external_hotrunner = data['funcConfig']['99']['status']
    if activate_external_hotrunner:
        external_hotrunner_num = int(data['extHotrunnerNum'])
    else:
        external_hotrunner_num = 0
    psg_hotrunner = data['funcConfig']['98']['status']

    if data['type'].upper() == 'ZES':
        imm_type = 'ZE' + clamp_force + 's-' + injection
    elif data['type'].upper() == 'ZE':
        imm_type = 'ZE' + clamp_force + '-' + injection
    elif data['type'].upper() == 'VE2S':
        imm_type = 'VE' + clamp_force + 'IIs-' + injection
    elif data['type'].upper() == 'VE2':
        imm_type = 'VE' + clamp_force + 'II-' + injection

    # 增加一个外层时间戳文件夹，用来阻止浏览器缓存文件
    dir_name = ''.join(str(time.time()).split('.'))
    wrap_dir = CACHE_FILE_DIR + dir_name + '/'
    wrap_url = URL_DIR + dir_name + '/'
    os.mkdir(wrap_dir)

    io_file_path = wrap_dir + evaluation_num + customer + imm_type + '.xlsx'
    io_url = wrap_url + evaluation_num + customer + imm_type + '.xlsx'

    print('creating io.xlsx, pls wait....')
    iomaker = IOMaker(imm_type=data['type'],
                      board_1_modules_ios=board_1_modules_ios,
                      board_2_modules_ios=board_2_modules_ios,
                      evaluation_num=evaluation_num,
                      production_num=production_num,
                      type_string=type_string,
                      customer=customer,
                      safety_standard=safety_standard,
                      technical_clause=technical_clause,
                      dual_inj=dual_inj,
                      external_hotrunner_num=external_hotrunner_num,
                      energy_dee=energy_dee,
                      varan_conn_module_pos=varan_conn_module_pos,
                      psg_hotrunner=psg_hotrunner,
                      main_board_modified_io=main_board_modified_io)
    if func_output1 != 0:
        iomaker.func1Config(func_output1)
    if func_output2 != 0:
        iomaker.func2Config(func_output2)
    iomaker.createFile(io_file_path)

    return jsonify({'status': 'success', 'url': io_url})

@app.route('/api/io/createconfigfile', methods=['POST'])
def createConfigFile():
    '''
        生成配置文件(.zip)
        同样只支持主底板和扩展底板一的编辑，更多的配置请自行特殊制作支持
        必须严格按照网页传输数据进行编程
        * 2019.06.13: （Bug fix）当计算得到两份重名文件时，由于浏览器缓存原因，将下载得到两份一样的文件
    '''
    data = request.get_json()
    client_ip = request.remote_addr
    record_info = 'IP: ' + client_ip + '创建配置文件：\n'
    record_info += request.data.decode()
    log.record(ip=client_ip, event='创建配置文件', description=request.data.decode())

    # 将post得到的数据整理成规范格式的数据
    board_1_modules_ios = []
    board_1 = data['boardModules1']
    board_1_ios = data['boardModulesIOs1']
    for idx in range(len(board_1)):
        if board_1[idx] != '':
            board_1_modules_ios.append([board_1[idx], board_1_ios[idx]])

    board_2_modules_ios = []
    board_2 = data['boardModules2']
    board_2_ios = data['boardModulesIOs2']
    for idx in range(len(board_2)):
        if board_2[idx] != '':
            board_2_modules_ios.append([board_2[idx], board_2_ios[idx]])

    customer = data['customer']

    # 硬件配置文件
    ce_standard = data['ceStandard']
    varan_conn_module_pos = data['varanConnModulePos']
    e73_safety = data['funcConfig']['3']['status']
    energy_dee = data['funcConfig']['5']['status']
    # 默认主底板修改的IO
    main_board_modified_io = data['mainBoardModifiedIo']

    # 安全继电器文件
    nor_pilz = data['pilzNor']
    e73_pilz = data['pilzE73']
    if not ce_standard or nor_pilz == '其他':
        nor_pilz = None
    if not e73_safety or e73_pilz == '其他':
        e73_pilz = None

    clamp_force = data['clampForce']
    injection = data['injection']

    # 下面开始生成文件路径，创建目录
    imm_type = ''
    zip_file_path = ''
    zip_file_url = ''
    if data['type'].upper() == 'ZES':
        imm_type = 'ZE' + clamp_force + 's-' + injection
    elif data['type'].upper() == 'ZE':
        imm_type = 'ZE' + clamp_force + '-' + injection
    elif data['type'].upper() == 'VE2S':
        imm_type = 'VE' + clamp_force + 'IIs-' + injection
    elif data['type'].upper() == 'VE2':
        imm_type = 'VE' + clamp_force + 'II-' + injection
    # 增加一个外层时间戳文件夹，用来阻止浏览器缓存文件
    dir_name = ''.join(str(time.time()).split('.'))
    wrap_dir = CACHE_FILE_DIR + dir_name + '/'
    wrap_url = URL_DIR + dir_name + '/'
    os.mkdir(wrap_dir)
    if ce_standard:
        dst_file_dir = wrap_dir + data['evaluationNum'] + customer + imm_type + '(CE)/'
        zip_file_path = wrap_dir + data['evaluationNum'] + customer + imm_type + '(CE).zip'
        zip_file_url = wrap_url + data['evaluationNum'] + customer + imm_type + '(CE).zip'
    else:
        dst_file_dir = wrap_dir + data['evaluationNum'] + customer + imm_type + '/'
        zip_file_path = wrap_dir + data['evaluationNum'] + customer + imm_type + '.zip'
        zip_file_url = wrap_url + data['evaluationNum'] + customer + imm_type + '.zip'
    if os.path.isdir(dst_file_dir):
        shutil.rmtree(dst_file_dir)
    os.mkdir(dst_file_dir)

    # 功能配置选项，注意key值和configfile.py中FcfFileMaker中属性名字对应
    functions = {}
    # functions['injSig'] = data['funcConfig']['1']['status']
    # functions['chargeSig'] = data['funcConfig']['2']['status']
    func_output1 = data['funcOutput1']
    func_output2 = data['funcOutput2']
    functions['dee'] = data['funcConfig']['5']['status']
    functions['internalHotrunnerNum'] = data['intHotrunnerNum']
    functions['valve'] = data['funcConfig']['101']['status']
    functions['air'] = data['funcConfig']['102']['status']
    functions['core'] = data['funcConfig']['103']['status']
    functions['progio'] = data['funcConfig']['104']['status']

    fcfmaker = FcfFileMaker(imm_type=data['type'],
                            functions=functions,
                            ce_standard=ce_standard,
                            dst_file_dir=dst_file_dir,
                            func_output1=func_output1,
                            func_output2=func_output2)
    if fcfmaker.createFile() != 0:
        return jsonify({'status': 'failure', 'description': '功能配置文件生成失败'})
    sysmaker = SysFileMaker(ce_standard=ce_standard,
                            clamp_force=clamp_force,
                            dst_file_dir=dst_file_dir)
    if sysmaker.createFile() != 0:
        return jsonify({'status': 'failure', 'description': '系统文件生成失败'})
    hkmaker = HkFileMaker(imm_type=data['type'],
                          board_1_modules_ios=board_1_modules_ios,
                          board_2_modules_ios=board_2_modules_ios,
                          dst_file_dir=dst_file_dir,
                          ce_standard=ce_standard,
                          varan_module_pos=varan_conn_module_pos,
                          energy_dee=energy_dee,
                          main_board_modified_io=main_board_modified_io)

    ret_status = hkmaker.createFile()
    if ret_status < 0:
        if ret_status == -1:
            error_description = '标准程序不支持的模块配置'
        elif ret_status == -2:
            error_description = '后台在复制硬件配置文件时候发生了严重错误！请检查后台程序'
        else:
            error_description = '检查到重复配置的IO点'
        return jsonify({'status': 'failure', 'description': '硬件配置文件生成失败：' + error_description})
    if ce_standard or e73_safety:
        mpnozmaker = SafetyFileMaker(nor_pilz=nor_pilz,
                                     e73_pilz=e73_pilz,
                                     dst_file_dir=dst_file_dir
                                     )
        if mpnozmaker.createFile() != 0:
            return jsonify({'status': 'failure', 'description': '安全继电器（或E73）文件生成失败'})
    createZip(dst_file_dir, zip_file_path)

    return jsonify({'status': 'success', 'url': zip_file_url})

@app.route('/api/io/allio', methods=['GET'])
def getAllIo():
    ret_data = {'DI': [], 'DO': [], 'AI': [], 'AO': [], 'TI': [], 'TO': []}
    t_di = TableManager('digital_input', IO_INFO_DB_PATH)
    t_do = TableManager('digital_output', IO_INFO_DB_PATH)
    t_ai = TableManager('analog_input', IO_INFO_DB_PATH)
    t_ao = TableManager('analog_output', IO_INFO_DB_PATH)
    t_ti = TableManager('temperature_input', IO_INFO_DB_PATH)
    t_to = TableManager('temperature_output', IO_INFO_DB_PATH)
    for i in range(1, IOS_AMOUNT['DI']+1):
        ret_data['DI'].append(t_di.displayBriefData(i, 'CName')[0])
    for i in range(1, IOS_AMOUNT['DO'] + 1):
        ret_data['DO'].append(t_do.displayBriefData(i, 'CName')[0])
    for i in range(1, IOS_AMOUNT['AI']+1):
        ret_data['AI'].append(t_ai.displayBriefData(i, 'CName')[0])
    for i in range(1, IOS_AMOUNT['AO']+1):
        ret_data['AO'].append(t_ao.displayBriefData(i, 'CName')[0])
    for i in range(1, IOS_AMOUNT['TI']+1):
        ret_data['TI'].append(t_ti.displayBriefData(i, 'CName')[0])
    for i in range(1, IOS_AMOUNT['TO']+1):
        ret_data['TO'].append(t_to.displayBriefData(i, 'CName')[0])
    return jsonify(ret_data)

@app.route('/api/io/stdio', methods = ['GET'])
def getStdIo():
    imm_type = request.args.get('type')
    ce_standard = request.args.get('ceStandard')
    if ce_standard is None or ce_standard == 'false':
        # GET方式传递的Boolean有问题！得到的是false而不是False
        ce_standard = False
    else:
        ce_standard = True
    hk_info = HkFileMaker(imm_type=imm_type, ce_standard=ce_standard)

    return jsonify({'status': 'success', 'stdIo': hk_info.getStdIoInfo()})

@app.route('/api/io/cfgadvice', methods=['GET'])
def getIoConfigAdvice():
    pass

# 避免频繁搜索数据库获取IO长度，这里一次性读取掉所有IO的数目
# 通过函数中获取，可能可以尽早销毁这些被创建的TableManager
def _getIoAmount():
    t_ios = {
        'DI': TableManager('digital_input', IO_INFO_DB_PATH),
        'DO': TableManager('digital_output', IO_INFO_DB_PATH),
        'AI': TableManager('analog_input', IO_INFO_DB_PATH),
        'AO': TableManager('analog_output', IO_INFO_DB_PATH),
        'TI': TableManager('temperature_input', IO_INFO_DB_PATH),
        'TO': TableManager('temperature_output', IO_INFO_DB_PATH)
    }
    return {
        'DI': len(t_ios['DI'].getAllId()),
        'DO': len(t_ios['DO'].getAllId()),
        'AI': len(t_ios['AI'].getAllId()),
        'AO': len(t_ios['AO'].getAllId()),
        'TI': len(t_ios['TI'].getAllId()),
        'TO': len(t_ios['TO'].getAllId())
    }


IOS_AMOUNT = _getIoAmount()