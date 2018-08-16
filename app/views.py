from flask import request, send_file, jsonify
import os
import shutil
from app import app
from app.sqljob import TableManager
from app.iomaker import IOMaker
from app.configfile import HkFileMaker, FcfFileMaker, SysFileMaker, createZip


@app.route('/', methods=['GET', 'POST'])
def home():
    return send_file("./static/index.html")

@app.route('/io', methods=['GET'])
def getIo():
    io_type = request.args.get('type')
    start_id = int(request.args.get('start'))
    end_id = int(request.args.get('end'))
    # io_type可以是'di', 'do', 'ai', 'ao', 'ti', 'to'
    if io_type == 'di':
        t_io = TableManager('digital_input', './app/libfiles/data.db')
    elif io_type == 'do':
        t_io = TableManager('digital_output', './app/libfiles/data.db')
    elif io_type == 'ai':
        t_io = TableManager('analog_input', './app/libfiles/data.db')
    elif io_type == 'ao':
        t_io = TableManager('analog_output', './app/libfiles/data.db')
    elif io_type == 'ti':
        t_io = TableManager('temperature_input', './app/libfiles/data.db')
    else:
        t_io = TableManager('temperature_output', './app/libfiles/data.db')
    ret_data = {}
    ret_data['amount'] = ios_amount[io_type]
    ret_data['ios'] = {}
    if start_id > end_id or start_id > ret_data['amount']:
        return jsonify(ret_data)
    if end_id > ret_data['amount']:
        end_id = ret_data['amount']
    for id in range(start_id, end_id + 1):
        ret_data['ios'][str(id)] = t_io.displayBriefData(id, 'CName')[0]

    return jsonify(ret_data)

@app.route('/big', methods=['GET'])
def getBigIo():
    # 获取大机选配CIO021或CIO011的IO点配置信息
    # 数据返回格式为{'name': 'CIO021(或CIO011)', ios: {'di3': '83--开门', ..., 'do2': '113--润滑马达2'}}
    cio021_io = {
        'di3': 83,
        'di4': 84,
        'di5': 85,
        'di6': 97,
        'di7': 98,
        'di8': 99,
        'do1': 97,
        'do2': 98,
        'do3': 113
    }
    if request.args.get('type').upper() == 'VE2':
        ret_data = {'name': 'CIO011', 'ios': {}}
    else:
        ret_data = {'name': 'CIO021', 'ios': {}}
    t_di = TableManager('digital_input', './app/libfiles/data.db')
    t_do = TableManager('digital_output', './app/libfiles/data.db')
    for k, v in cio021_io.items():
        if k.startswith('di'):
            ret_data['ios'][k] = str(v) + '--' + t_di.displayBriefData(v, 'CName')[0]
        if k.startswith('do'):
            ret_data['ios'][k] = str(v) + '--' + t_do.displayBriefData(v, 'CName')[0]
    return jsonify(ret_data)

@app.route('/createxlxs', methods=['POST'])
def createIoFile():
    '''
        生成IO表文件(.xlsx)
        目前后台只支持主底板和扩展底板一的编辑
        根据网页POST数据格式，进行数据处理。
        必须严格参照网页传输的数据进行编程
    '''
    # data是一个dict对象
    data = request.get_json()

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
    func1_to_inj_signal = data['funcConfig']['1']['status']
    func2_to_charge_signal = data['funcConfig']['2']['status']
    e73_safety = data['funcConfig']['3']['status']
    nozzle_to_valve = data['funcConfig']['4']['status']
    # 能耗模块DEE是否启用
    energy_dee = data['funcConfig']['5']['status']
    # Varan连接模块如果启用，安装在KEB之后(0)之前(1)
    varan_conn_module_pos = data['varanConnModulePos']
    # 外置热流道是否激活，及组数
    # 注意网页端提交的功能序号可能随功能增加而改变，注意 data['funcConfig']['?']['status]中的序号('?')需要随之更新
    activate_external_hotrunner = data['funcConfig']['666']['status']
    if activate_external_hotrunner:
        external_hotrunner_num = int(data['extHotrunnerNum'])
    else:
        external_hotrunner_num = 0

    if data['type'].upper() == 'ZES':
        imm_type = 'ZE' + clamp_force + 's-' + injection
    elif data['type'].upper() == 'ZE':
        imm_type = 'ZE' + clamp_force + '-' + injection
    elif data['type'].upper() == 'VE2S':
        imm_type = 'VE' + clamp_force + 'IIs-' + injection
    elif data['type'].upper() == 'VE2':
        imm_type = 'VE' + clamp_force + 'II-' + injection

    # 对于python运行环境来说，此时工作路径为  /MyProj
    io_file_path = './app/static/cache/' + evaluation_num + customer + imm_type + '.xlsx'
    # 对于Flask框架来说，此时工作路径为  /app   且所有HTTP请求的文件必须位于 /app/static目录之下
    io_url = './static/cache/' + evaluation_num + customer + imm_type + '.xlsx'

    print('wait....')
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
                      varan_conn_module_pos=varan_conn_module_pos)
    if func1_to_inj_signal:
        iomaker.func1ToInjSignal()
    if func2_to_charge_signal:
        iomaker.func2ToChargeSignal()
    if nozzle_to_valve:
        iomaker.nozzleToValve()
    if e73_safety:
        iomaker.e73Safety()
    iomaker.createFile(io_file_path)

    return jsonify({'status': 'ok', 'url': io_url})

@app.route('/createconfigfile', methods=['POST'])
def createConfigFile():
    '''
        生成配置文件(.hk)
        同样只支持主底板和扩展底板一的编辑，更多的配置请自行特殊制作支持
        必须严格按照网页传输数据进行编程
    '''
    data = request.get_json()

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

    # 硬件配置文件
    ce_standard = data['ceStandard']
    varan_conn_module_pos = data['varanConnModulePos']
    e73_safety = data['funcConfig']['3']['status']
    energy_dee = data['funcConfig']['5']['status']

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
    if ce_standard:
        dst_file_dir = './app/static/cache/' + data['evaluationNum'] + imm_type + '(CE)/'
        zip_file_path = './app/static/cache/' + data['evaluationNum'] + imm_type + '(CE).zip'
        zip_file_url = './static/cache/' + data['evaluationNum'] + imm_type + '(CE).zip'
    else:
        dst_file_dir = './app/static/cache/' + data['evaluationNum'] + imm_type + '/'
        zip_file_path = './app/static/cache/' + data['evaluationNum'] + imm_type + '.zip'
        zip_file_url = './static/cache/' + data['evaluationNum'] + imm_type + '.zip'
    if os.path.isdir(dst_file_dir):
        shutil.rmtree(dst_file_dir)
    os.mkdir(dst_file_dir)

    # 功能配置选项，注意key值和configfile.py中的名字对应
    functions = {}
    functions['injSig'] = data['funcConfig']['1']['status']
    functions['chargeSig'] = data['funcConfig']['2']['status']
    functions['dee'] = data['funcConfig']['5']['status']
    functions['internalHotrunnerNum'] = data['intHotrunnerNum']

    fcfmaker = FcfFileMaker(imm_type=data['type'],
                            functions=functions,
                            ce_standard=ce_standard,
                            dst_file_dir=dst_file_dir)
    fcfmaker.createFile()
    sysmaker = SysFileMaker(ce_standard=ce_standard,
                            clamp_force=clamp_force,
                            dst_file_dir=dst_file_dir)
    sysmaker.createFile()
    hkmaker = HkFileMaker(imm_type=data['type'],
                          board_1_modules_ios=board_1_modules_ios,
                          board_2_modules_ios=board_2_modules_ios,
                          dst_file_dir=dst_file_dir,
                          ce_standard=ce_standard,
                          varan_module_pos=varan_conn_module_pos,
                          e73=e73_safety,
                          energy_dee=energy_dee)
    hkmaker.createFile()
    createZip(dst_file_dir, zip_file_path)

    return jsonify({'status': 'success', 'url': zip_file_url, 'hwfileInfo': hkmaker.getConfigInfo()})




# 避免频繁搜索数据库获取IO长度，这里一次性读取掉所有IO的数目
# 通过函数中获取，可能可以尽早销毁这些被创建的TableManager
def _getIoAmount():
    t_ios = {
        'di': TableManager('digital_input', './app/libfiles/data.db'),
        'do': TableManager('digital_output', './app/libfiles/data.db'),
        'ai': TableManager('analog_input', './app/libfiles/data.db'),
        'ao': TableManager('analog_output', './app/libfiles/data.db'),
        'ti': TableManager('temperature_input', './app/libfiles/data.db'),
        'to': TableManager('temperature_output', './app/libfiles/data.db')
    }
    return {
        'di': len(t_ios['di'].getAllId()),
        'do': len(t_ios['do'].getAllId()),
        'ai': len(t_ios['ai'].getAllId()),
        'ao': len(t_ios['ao'].getAllId()),
        'ti': len(t_ios['ti'].getAllId()),
        'to': len(t_ios['to'].getAllId())
    }


ios_amount = _getIoAmount()
