from flask import request, send_file, jsonify
import shutil
from app import app
from app.sqljob import TableManager
from app.iomaker import IOMaker
from app.configfile import HkFileMaker, FcfFileMaker, SysFileMaker, SafetyFileMaker, createZip
from app.pathinfo import *
from app.softupdater import Updater


@app.route('/', methods=['GET', 'POST'])
def home():
    return send_file(ENTRY_HTML_PATH)

# 没有下面404处理，会导致vue-router在history模式下一刷新就404错误
@app.errorhandler(404)
def pageNotFound(e):
    return send_file(ENTRY_HTML_PATH)


# ##################################### IO #################################
@app.route('/io', methods=['GET'])
def getIo():
    io_type = request.args.get('type')
    start_id = int(request.args.get('start'))
    end_id = int(request.args.get('end'))
    # io_type可以是'di', 'do', 'ai', 'ao', 'ti', 'to'
    if io_type == 'di':
        t_io = TableManager('digital_input', IO_INFO_DB_PATH)
    elif io_type == 'do':
        t_io = TableManager('digital_output', IO_INFO_DB_PATH)
    elif io_type == 'ai':
        t_io = TableManager('analog_input', IO_INFO_DB_PATH)
    elif io_type == 'ao':
        t_io = TableManager('analog_output', IO_INFO_DB_PATH)
    elif io_type == 'ti':
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
    t_di = TableManager('digital_input', IO_INFO_DB_PATH)
    t_do = TableManager('digital_output', IO_INFO_DB_PATH)
    for k, v in cio021_io.items():
        if k.startswith('di'):
            ret_data['ios'][k] = str(v) + '--' + t_di.displayBriefData(v, 'CName')[0]
        if k.startswith('do'):
            ret_data['ios'][k] = str(v) + '--' + t_do.displayBriefData(v, 'CName')[0]
    return jsonify(ret_data)

@app.route('/pilzlist', methods=['GET'])
def getPilzList():
    ret_data = {'normal': [], 'e73': []}
    for file_name in os.listdir(NOR_SAFETY_RELAY_FILE_DIR):
        ret_data['normal'].append(file_name)
    for file_name in os.listdir(E73_SAFETY_RELAY_FILE_DIR):
        ret_data['e73'].append(file_name)

    ret_data['normal'].append('其他')
    ret_data['e73'].append('其他')
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
    if e73_safety or data['type'].upper() == 'VE2':
        # 7号点改可编程输出与E73冲突，且VE2不允许修改7号点
        mold_slider = False
    else:
        mold_slider = data['funcConfig']['6']['status']
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

    io_file_path = CACHE_FILE_DIR + evaluation_num + customer + imm_type + '.xlsx'
    io_url = URL_DIR + evaluation_num + customer + imm_type + '.xlsx'

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
                      varan_conn_module_pos=varan_conn_module_pos)
    if func1_to_inj_signal:
        iomaker.func1ToInjSignal()
    if func2_to_charge_signal:
        iomaker.func2ToChargeSignal()
    if nozzle_to_valve:
        iomaker.nozzleToValve()
    if e73_safety and data['type'].upper() != 'VE2':
        # VE2的E73需要自己配置
        iomaker.e73Safety()
    if mold_slider:
        iomaker.moldSlider()
    iomaker.createFile(io_file_path)

    return jsonify({'status': 'success', 'url': io_url})

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
    if e73_safety or data['type'].upper() == 'VE2':
        mold_slider = False
    else:
        mold_slider = data['funcConfig']['6']['status']

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
    if ce_standard:
        dst_file_dir = CACHE_FILE_DIR + data['evaluationNum'] + imm_type + '(CE)/'
        zip_file_path = CACHE_FILE_DIR + data['evaluationNum'] + imm_type + '(CE).zip'
        zip_file_url = URL_DIR + data['evaluationNum'] + imm_type + '(CE).zip'
    else:
        dst_file_dir = CACHE_FILE_DIR + data['evaluationNum'] + imm_type + '/'
        zip_file_path = CACHE_FILE_DIR + data['evaluationNum'] + imm_type + '.zip'
        zip_file_url = URL_DIR + data['evaluationNum'] + imm_type + '.zip'
    if os.path.isdir(dst_file_dir):
        shutil.rmtree(dst_file_dir)
    os.mkdir(dst_file_dir)

    # 功能配置选项，注意key值和configfile.py中FcfFileMaker中属性名字对应
    functions = {}
    functions['injSig'] = data['funcConfig']['1']['status']
    functions['chargeSig'] = data['funcConfig']['2']['status']
    functions['dee'] = data['funcConfig']['5']['status']
    functions['internalHotrunnerNum'] = data['intHotrunnerNum']
    functions['valve'] = data['funcConfig']['7']['status']
    functions['air'] = data['funcConfig']['8']['status']
    functions['core'] = data['funcConfig']['9']['status']
    functions['progio'] = data['funcConfig']['10']['status']

    fcfmaker = FcfFileMaker(imm_type=data['type'],
                            functions=functions,
                            ce_standard=ce_standard,
                            dst_file_dir=dst_file_dir)
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
                          e73=e73_safety,
                          energy_dee=energy_dee,
                          mold_slider=mold_slider)
    # debug时候查看硬件修改
    # print(hkmaker.getConfigInfo())
    if hkmaker.createFile() < 0:
        return jsonify({'status': 'failure', 'description': '硬件配置文件生成失败'})
    if ce_standard or e73_safety:
        mpnozmaker = SafetyFileMaker(nor_pilz=nor_pilz,
                                     e73_pilz=e73_pilz,
                                     dst_file_dir=dst_file_dir
                                     )
        if mpnozmaker.createFile() != 0:
            return jsonify({'status': 'failure', 'description': '安全继电器（或E73）文件生成失败'})
    createZip(dst_file_dir, zip_file_path)

    return jsonify({'status': 'success', 'url': zip_file_url})


# 避免频繁搜索数据库获取IO长度，这里一次性读取掉所有IO的数目
# 通过函数中获取，可能可以尽早销毁这些被创建的TableManager
def _getIoAmount():
    t_ios = {
        'di': TableManager('digital_input', IO_INFO_DB_PATH),
        'do': TableManager('digital_output', IO_INFO_DB_PATH),
        'ai': TableManager('analog_input', IO_INFO_DB_PATH),
        'ao': TableManager('analog_output', IO_INFO_DB_PATH),
        'ti': TableManager('temperature_input', IO_INFO_DB_PATH),
        'to': TableManager('temperature_output', IO_INFO_DB_PATH)
    }
    return {
        'di': len(t_ios['di'].getAllId()),
        'do': len(t_ios['do'].getAllId()),
        'ai': len(t_ios['ai'].getAllId()),
        'ao': len(t_ios['ao'].getAllId()),
        'ti': len(t_ios['ti'].getAllId()),
        'to': len(t_ios['to'].getAllId())
    }


IOS_AMOUNT = _getIoAmount()


# ##################################### Version #################################
@app.route('/queryversions', methods=['GET'])
def getVersion():
    '''
        根据请求的版本类型以及版本区间（不是数据库的id号）返回版本数据
        当某个版本类型下的所有版本数据按一定顺序（这里按名字降序排列）后，取
        位于第start_seq和end_seq之间的版本数据
        :return 格式如 {'itemsNum': 123, 'items': {'client': xxx, 'version': xxx , ...}}
    '''
    soft_type = request.args.get('softType')
    start_seq = int(request.args.get('start'))
    end_seq = int(request.args.get('end'))
    table_name = 't_' + soft_type
    t_soft = TableManager(table_name, SOFTWARE_VERSION_INFO_DB_PATH)
    ret_data = {'itemsNum': len(ALL_VERS_ID[soft_type]), 'items': {}}
    key = 0
    for soft_id in ALL_VERS_ID[soft_type][start_seq: end_seq]:
        # 即使end_seq超过ALL_VERS_ID的长度也无所谓，不会影响结果
        ret_data['items'][key] = t_soft.displayDetailedData(soft_id)
        key += 1
    return jsonify(ret_data)


# 需要遍历数据库和xls表，并且对比两者的差别，非常费时
# 检测更新需要遍历数据库和xls表，为了避免确认更新时，重复检测更新
# 将下面变量设为全局变量
updaters = {
    'V01': Updater('t_V01', 'V01'),
    'V02': Updater('t_V02', 'V02'),
    'V03V04': Updater('t_V03V04', 'V03&V04'),
    'V05': Updater('t_V05', 'V05'),
    'T05': Updater('t_T05', 'T05'),
}
@app.route('/checkupdate', methods=['GET'])
def checkUpdate():
    '''
        检查某类版本的更新信息
        如果找不到或无法打开'软件版本登记表.xls'文件，这里返回状态为失败。
        :return: 成功返回格式如 {'status': success, 'newVers': [{'client': xx, 'version': xx, ...}, {...}, ,,]}
                  失败返回格式如 {'status': failure, 'description': 'xxxx'}
    '''
    global ALL_VERS_ID, updaters
    soft_type = request.args.get('softType')
    vers_ready_to_update = updaters[soft_type].getUpdateInfo()
    if vers_ready_to_update is None:
        return jsonify({'status': 'failure', 'description': '无法打开xls文件路径，检查后台 "软件版本登记表.xls" 文件路径'})
    return jsonify({'status': 'success', 'newVers': vers_ready_to_update})

@app.route('/startupdate', methods=['GET'])
def startUpdate():
    global updaters, ALL_VERS_ID
    soft_type = request.args.get('softType')
    if updaters[soft_type].startUpdate() is False:
        return jsonify({'status': 'failure', 'description': '更新信息已过期，请重试'})
    ALL_VERS_ID = _getAllVersionsId()
    return jsonify({'status': 'success'})

# 以降序获取所有版本的ID号
# 避免频繁搜索数据库，这里一次性读取掉所有版本ID号
def _getAllVersionsId():
    t_vers = {
        't_V01': TableManager('t_V01', SOFTWARE_VERSION_INFO_DB_PATH),
        't_V02': TableManager('t_V02', SOFTWARE_VERSION_INFO_DB_PATH),
        't_V03V04': TableManager('t_V03V04', SOFTWARE_VERSION_INFO_DB_PATH),
        't_V05': TableManager('t_V05', SOFTWARE_VERSION_INFO_DB_PATH),
        't_T05': TableManager('t_T05', SOFTWARE_VERSION_INFO_DB_PATH)
    }
    return {
        'V01': t_vers['t_V01'].getAllId('version', desc=True),
        'V02': t_vers['t_V02'].getAllId('version', desc=True),
        'V03V04': t_vers['t_V03V04'].getAllId('version', desc=True),
        'V05': t_vers['t_V05'].getAllId('version', desc=True),
        'T05': t_vers['t_T05'].getAllId('version', desc=True)
    }


ALL_VERS_ID = _getAllVersionsId()

@app.route('/downloadsrccode', methods=['GET'])
def downloadSrcCode():
    '''
        为网页端准备下载文件（根据提供的路径复制文件到cache/），然后返回url提供下载
    '''
    src_path = request.args.get('path')
    print(src_path)
    if not os.path.isfile(src_path):
        return jsonify({'status': 'failure', 'description': '数据库路径无效在本服务器上无效，'})
    file_name = os.path.basename(src_path)
    dst_path = os.path.join(CACHE_FILE_DIR, file_name)
    shutil.copy(src_path, dst_path)
    if not os.path.isfile(dst_path):
        return jsonify({'status': 'failure', 'description': '后台源程序文件复制失败，请重试'})
    src_code_url = os.path.join(URL_DIR, file_name)
    return jsonify({'status': 'success', 'url': src_code_url})
