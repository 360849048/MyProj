from flask import request, send_file, jsonify
from app import app
from app.sqljob import TableManager
from app.iomaker import IOMaker
from app.configfile import HardwareConfigFile


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
    board_1_modules = []
    board_1 = data['boardModules1']
    board_1_ios = data['boardModulesIOs1']
    for idx in range(len(board_1)):
        if board_1[idx] != '':
            board_1_modules.append([board_1[idx], board_1_ios[idx]])

    board_2_modules = []
    board_2 = data['boardModules2']
    board_2_ios = data['boardModulesIOs2']
    for idx in range(len(board_2)):
        if board_2[idx] != '':
            board_2_modules.append([board_2[idx], board_2_ios[idx]])

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
                      board_1_modules=board_1_modules,
                      board_2_modules=board_2_modules,
                      evaluation_num=evaluation_num,
                      production_num=production_num,
                      type_string=type_string,
                      customer=customer,
                      safety_standard=safety_standard,
                      technical_clause=technical_clause,
                      dual_inj=dual_inj,
                      external_hotrunner_num=external_hotrunner_num,
                      energy_dee=energy_dee)
    if func1_to_inj_signal:
        iomaker.func1ToInjSignal()
    if func2_to_charge_signal:
        iomaker.func2ToChargeSignal()
    if nozzle_to_valve:
        iomaker.nozzleToValve()
    if e73_safety:
        iomaker.e73Safety()
    iomaker.createIOFile(io_file_path)

    return jsonify({'status': 'ok', 'ioFileUrl': io_url})

@app.route('/createhkfile', methods=['POST'])
def createHkFile():
    '''
        生成硬件配置文件(.hk)
        同样只支持主底板和扩展底板一的编辑，更多的配置请自行特殊制作支持
        对POST过来的数据进行处理，
        必须严格按照网页传输数据进行编程
    '''
    # 整理POST得到的数据，目标格式如下：
    #   io_config_info = {'DI':{41: 41, 73: 81}, 'DO': {}, 'AI': {}, ... }    key是IO的序号(io_seq)，value是IO的位置(io_pos)
    #   module_config_info = {'1': [], '2': [], '3': [1, 3, 0, 0], '4': [5, 3, 0]}     key是board的序号，value是底板上的模块序号数，这里不显示Varan模块
    #   varan_config_info = [3, 5]   Varan总线上依次的模块名： 0:未配置  1:CIV512  2:CIV521  3:CMM10X  4:DEE021  5:F6
    io_config_info = {'DI': {}, 'DO': {}, 'AI': {}, 'AO': {}, 'TI': {}, 'TO': {}}
    module_config_info = {'1': [0], '2': [0, 0, 0], '3': [0, 0, 0, 0], '4': [0, 0, 0]}
    varan_config_info = [3, 5]

    data = request.get_json()
    imm_type = data['type'].upper()
    # 统计选配模块的出现次数
    # 统计结果的格式如：board_1_modules_count = {'CDM163': 2, 'CTO163': 1}
    board_1_modules_count = {}
    board_1_modules = data['boardModules1']
    board_1_modules_ios = data['boardModulesIOs1']
    for idx in range(len(board_1_modules)):
        module = board_1_modules[idx]
        # 非VE2机的主底板扩展槽内容检测
        if module != '' and imm_type != 'VE2':
            # IO位置的偏移量
            board_1_io_pos_offset = {'DI': 0, 'DO': 0, 'AI': 0, 'AO': 0, 'TI': 0, 'TO': 0}
            if module not in board_1_modules_count:
                board_1_modules_count[module] = 1
            else:
                board_1_modules_count[module] += 1
            # 根据不同的模块，对应不同的起始位置，比如第一块CTO163，DO从41开始
            if module.upper() == 'CTO163':
                # 标准程序支持至多2块CTO163
                if board_1_modules_count[module] == 1:
                    board_1_io_pos_offset['DO'] = 41 - 1
                    module_config_info['3'][idx] = 2
                elif board_1_modules_count[module] == 2:
                    board_1_io_pos_offset['DO'] = 57 - 1
                    module_config_info['3'][idx] = 3
                else:
                    print('Error: 标准程序CMM102主底板支持至多2块CTO163')
                    io_config_info = {'DI': {}, 'DO': {}, 'AI': {}, 'AO': {}, 'TI': {}, 'TO': {}}
                    break
            if module.upper == 'CDI163':
                # 标准程序只支持至多1块CDI163
                if board_1_modules_count[module] == 1:
                    board_1_io_pos_offset['DI'] = 57 - 1
                    module_config_info['3'][idx] = 1
                else:
                    print('Error: 标准程序CMM102主底板支持至多1块CDI163')
                    io_config_info = {'DI': {}, 'DO': {}, 'AI': {}, 'AO': {}, 'TI': {}, 'TO': {}}
                    break
            if module.upper() == 'CDM163':
                # 标准程序只支持至多4块CDM163
                if board_1_modules_count[module] == 1:
                    board_1_io_pos_offset['DI'] = 81 - 1
                    board_1_io_pos_offset['DO'] = 81 - 1
                    module_config_info['3'][idx] = 7
                elif board_1_modules_count[module] == 2:
                    board_1_io_pos_offset['DI'] = 89 - 1
                    board_1_io_pos_offset['DO'] = 89 - 1
                    module_config_info['3'][idx] = 8
                elif board_1_modules_count[module] == 3:
                    board_1_io_pos_offset['DI'] = 97 - 1
                    board_1_io_pos_offset['DO'] = 97 - 1
                    module_config_info['3'][idx] = 9
                elif board_1_modules_count[module] == 4:
                    board_1_io_pos_offset['DI'] = 105 - 1
                    board_1_io_pos_offset['DO'] = 105 - 1
                    module_config_info['3'][idx] = 10
                else:
                    print('Error: 标注程序CMM102主底板只支持至多4块CDM163')
                    io_config_info = {'DI': {}, 'DO': {}, 'AI': {}, 'AO': {}, 'TI': {}, 'TO': {}}
                    break
            if module.upper() == 'CIO021':
                # 标准程序只支持至多1块CIO021
                if board_1_modules_count[module] == 1:
                    board_1_io_pos_offset['DI'] = 73 - 1
                    board_1_io_pos_offset['DO'] = 73 - 1
                    board_1_io_pos_offset['AI'] = 5 - 1
                    # TODO: AO起始位置未知
                    module_config_info['3'][idx] = 12
                else:
                    print('Error: 标注程序CMM102主底板只支持至多1块CIO021')
                    io_config_info = {'DI': {}, 'DO': {}, 'AI': {}, 'AO': {}, 'TI': {}, 'TO': {}}
                    break
            if module.upper() == 'CIO011':
                # 标准程序只支持至多1块CIO011
                if board_1_modules_count[module] == 1:
                    board_1_io_pos_offset['DI'] = 113 - 1
                    board_1_io_pos_offset['DO'] = 129 - 1
                    board_1_io_pos_offset['AI'] = 3 - 1
                    # TODO: AO起始位置未知
                    module_config_info['3'][idx] = 4
                else:
                    print('Error: 标注程序CMM102主底板只支持至多1块CIO011')
                    io_config_info = {'DI': {}, 'DO': {}, 'AI': {}, 'AO': {}, 'TI': {}, 'TO': {}}
                    break
            if module.upper() == 'CAI888':
                # 标准程序只支持3块CAI888
                if board_1_modules_count[module] == 1:
                    module_config_info['3'][idx] = 5
                elif board_1_modules_count[module] == 2:
                    module_config_info['3'][idx] = 6
                elif board_1_modules_count[module] == 2:
                    module_config_info['3'][idx] = 13
                else:
                    print('Error: 标准程序CMM102主底板只支持3块CAI888')

            for key, value in board_1_modules_ios[idx].items():
                # TODO: 这样简陋的解析数据容易出BUG
                io_type = key[:2].upper()
                io_seq = int(value)
                io_pos = int(key[2:]) + board_1_io_pos_offset[io_type]
                io_config_info[io_type][io_seq] = io_pos

    board_2_modules_count = {}
    # 去掉扩展底板一的Varan连接模块
    board_2_modules = data['boardModules2'][1:]
    board_2_modules_ios = data['boardModulesIOs2'][1:]
    for idx in range(len(board_2_modules)):
        module = board_2_modules[idx]
        # 非VE2机的主底板扩展槽内容检测
        if module != '' and imm_type != 'VE2':
            # IO位置的偏移量
            board_2_io_pos_offset = {'DI': 0, 'DO': 0, 'AI': 0, 'AO': 0, 'TI': 0, 'TO': 0}
            if module not in board_2_modules_count:
                board_2_modules_count[module] = 1
            else:
                board_2_modules_count[module] += 1
            # 根据不同的模块，对应不同的起始位置，比如第一块CTO163，DO从41开始
            if module.upper() == 'CTO163':
                # 标准程序支持至多2块CTO163
                if board_2_modules_count[module] == 1:
                    board_2_io_pos_offset['DO'] = 153 - 1
                    module_config_info['4'][idx] = 2
                elif board_2_modules_count[module] == 2:
                    board_2_io_pos_offset['DO'] = 169 - 1
                    module_config_info['4'][idx] = 3
                else:
                    print('Error: 标准程序CMM102扩展底板一支持至多2块CTO163')
                    io_config_info = {'DI': {}, 'DO': {}, 'AI': {}, 'AO': {}, 'TI': {}, 'TO': {}}
                    break
            if module.upper == 'CDI163':
                # 标准程序只支持至多2块CDI163
                if board_2_modules_count[module] == 1:
                    board_2_io_pos_offset['DI'] = 169 - 1
                    module_config_info['4'][idx] = 1
                elif board_2_modules_count[module] == 2:
                    board_2_io_pos_offset['DI'] = 217 - 1
                    module_config_info['4'][idx] = 14
                else:
                    print('Error: 标准程序CMM102扩展底板一支持至多2块CDI163')
                    io_config_info = {'DI': {}, 'DO': {}, 'AI': {}, 'AO': {}, 'TI': {}, 'TO': {}}
                    break
            if module.upper() == 'CDM163':
                # 标准程序只支持至多2块CDM163
                if board_2_modules_count[module] == 1:
                    board_2_io_pos_offset['DI'] = 185 - 1
                    board_2_io_pos_offset['DO'] = 185 - 1
                    module_config_info['4'][idx] = 4
                elif board_2_modules_count[module] == 2:
                    board_2_io_pos_offset['DI'] = 209 - 1
                    board_2_io_pos_offset['DO'] = 209 - 1
                    module_config_info['4'][idx] = 13
                else:
                    print('Error: 标注程序CMM102扩展底板一只支持至多2块CDM163')
                    io_config_info = {'DI': {}, 'DO': {}, 'AI': {}, 'AO': {}, 'TI': {}, 'TO': {}}
                    break
            if module.upper() == 'CIO021':
                # 标准程序只支持至多1块CIO021
                if board_2_modules_count[module] == 1:
                    board_2_io_pos_offset['DI'] = 193 - 1
                    board_2_io_pos_offset['DO'] = 193 - 1
                    # TODO: AI,AO起始位置未知
                    module_config_info['4'][idx] = 11
                else:
                    print('Error: 标注程序CMM102扩展底板一只支持至多1块CIO021')
                    io_config_info = {'DI': {}, 'DO': {}, 'AI': {}, 'AO': {}, 'TI': {}, 'TO': {}}
                    break
            if module.upper() == 'CIO011':
                # 标准程序只支持至多1块CIO011
                if board_2_modules_count[module] == 1:
                    board_2_io_pos_offset['DI'] = 201 - 1
                    board_2_io_pos_offset['DO'] = 201 - 1
                    # TODO: AI,AO起始位置未知
                    module_config_info['4'][idx] = 12
                else:
                    print('Error: 标注程序CMM102扩展底板一只支持至多1块CIO011')
                    io_config_info = {'DI': {}, 'DO': {}, 'AI': {}, 'AO': {}, 'TI': {}, 'TO': {}}
                    break
            if module.upper() == 'CAI888':
                # 标准程序只支持5块CAI888
                if board_2_modules_count[module] == 1:
                    module_config_info['4'][idx] = 5
                elif board_2_modules_count[module] == 2:
                    module_config_info['4'][idx] = 6
                elif board_2_modules_count[module] == 3:
                    module_config_info['4'][idx] = 7
                elif board_2_modules_count[module] == 4:
                    module_config_info['4'][idx] = 8
                elif board_2_modules_count[module] == 5:
                    module_config_info['4'][idx] = 9
                else:
                    print('Error: 标准程序CMM102扩展底板一只支持5块CAI888')

            for key, value in board_2_modules_ios[idx].items():
                # TODO: 这样简陋的解析数据容易出BUG
                io_type = key[:2].upper()
                io_seq = int(value)
                io_pos = int(key[2:]) + board_2_io_pos_offset[io_type]
                io_config_info[io_type][io_seq] = io_pos

    # 能耗模块DEE是否启用
    energy_dee = data['funcConfig']['5']['status']
    if energy_dee:
        varan_config_info = [3, 4, 5]
    # Varan连接模块
    varan_conn_module = data['boardModules2'][0]
    if varan_conn_module.upper() == 'CIV512':
        varan_config_info.append(1)
    elif varan_conn_module.upper() == 'CIV521':
        varan_config_info.append(2)
    else:
        pass
    # TI和TO配置容易出错，清空他们的配置信息
    io_config_info['TI'] = {}
    io_config_info['TO'] = {}
    print('module_config_info', module_config_info)
    print('io_config_info:', io_config_info)
    print('varan_config_info:', varan_config_info)
    hwmaker = HardwareConfigFile(imm_type=data['type'],
                                 io_config_info=io_config_info,
                                 module_config_info=module_config_info,
                                 varan_config_info=varan_config_info)
    hwmaker.modifyDstFile()

    return jsonify({'status': 'ok'})




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
