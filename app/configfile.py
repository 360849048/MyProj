import shutil
import re
import zipfile
from app.pathinfo import *


CMM103_IO_NUM = {'DI': 56, 'DO': 40, 'AI': 6, 'AO': 4, 'TI': 11, 'TO': 8}
MODULE_SYS_IO_NUM = {'DI': 56, 'DO': 40, 'AI': 3, 'AO': 2, 'TI': 8, 'TO': 8}

class HkFileMaker:
    def __init__(self, imm_type, ce_standard=False, board_1_modules_ios=None, board_2_modules_ios=None,
                 energy_dee=False, varan_module_pos=0, main_board_modified_io=None, std_file_dir=STD_HK_FILE_DIR,
                 dst_file_dir=CACHE_FILE_DIR):
        '''
            imm_type:           'ZEs', 'ZE', 'VE2', 'VE2s'
            board_1_modules_ios: [['CTO163', {'DO3': OutputID, ...}], ['CDM163', {'DI5': InputID, ...}], ...]
            board_2_modules_ios:    [['CTO163', {'DO3': OutputID, ...}], ['CDM163', {'DI5': InputID, ...}], ...]
            varan_module_pos:   0：CIV512等连接模块放在KEB之后； 1：CIV512等连接模块放在KEB之前
            main_board_modified_io: {'DI7': InputID, 'DO37': OutputID, ...}
        '''
        self.imm_type = imm_type
        self.board_1_modules_ios = board_1_modules_ios
        self.board_2_modules_ios = board_2_modules_ios
        self.dee = energy_dee
        self.varan_module_pos = int(varan_module_pos)
        if imm_type == 'VE2':
            self.std_io_num = MODULE_SYS_IO_NUM
        else:
            self.std_io_num = CMM103_IO_NUM

        if imm_type.endswith('s'):
            self.ce_standard = ce_standard
        else:
            self.ce_standard = False

        self.main_board_modified_io = main_board_modified_io
        # 清空HK文件中某些IO的位置信息
        # 因为如果仅仅按照io_config_info将IO点配置到各个新位置，原来老位置的IO点会残留。
        # 例如io_config_info: {'DI':{41: 53, 73: 81}, 'DO': {16: 23}, ...}，
        # 但是原先HK文件中，41号位置配置了80号IO，因此需要先将第80号IO写0，否则会导致多个IO配到同一个地方
        self.io_reset_info = {'DI': set(), 'DO': set(), 'AI': set(), 'AO': set(), 'TI': set(), 'TO': set()}

        # 为了生成文件的可靠性，只有status==0才允许某些操作
        # status: 0     正常
        # status: -1    找到了多份硬件配置文件
        # status: -2    配置的模块不符合标准程序，例如标准程序主底板最多支持2块CTO163，实际却配了3块
        # status: -3    将同一个IO配置到了多个地方
        self.status = 0

        # 根据机型以及安全标准确定 “标准硬件配置” 和 修改后的 “特殊硬件配置” 文件路径
        self.std_file_path = ''
        self.dst_file_path = ''
        for file_name in os.listdir(os.path.join(std_file_dir, self.imm_type)):
            if self.ce_standard is True:
                if 'BCD' in file_name and self.imm_type in file_name:
                    if self.std_file_path == '':
                        self.std_file_path = os.path.join(std_file_dir, self.imm_type, file_name)
                        self.dst_file_path = os.path.join(dst_file_dir, file_name)
                    else:
                        print("找到了好几份符合标准的硬件配置文件")
                        self.status = -1
                        break
            else:
                if self.imm_type in file_name and 'BCD' not in file_name:
                    if self.std_file_path == '':
                        self.std_file_path = os.path.join(std_file_dir, self.imm_type, file_name)
                        self.dst_file_path = os.path.join(dst_file_dir, file_name)
                    else:
                        print("找到了好几份符合标准的硬件配置文件")
                        self.status = -1
                        break

        self.io_config_info = {'DI': {}, 'DO': {}, 'AI': {}, 'AO': {}, 'TI': {}, 'TO': {}}
        self.module_config_info = {'1': [0], '2': [0, 0, 0], '3': [0, 0, 0, 0], '4': [0, 0, 0]}
        if self.imm_type != 'VE2':
            self.varan_config_info = [3, 5]
        else:
            self.varan_config_info = [0, 0, 0, 5]

    def _getConfigInfo(self):
        '''
            根据实际机器硬件配置文件记录的规矩，解析模块，IO配置信息
            io_config_info = {'DI':{41: 41, 73: 81}, 'DO': {}, 'AI': {}, ... }    key是IO的序号(io_seq)，value是IO的位置(io_pos)
            module_config_info = {'1': [], '2': [], '3': [1, 3, 0, 0], '4': [5, 3, 0]}     key是board的序号，value是底板上的模块序号数，这里不显示Varan模块
            varan_config_info = [3, 5]   Varan总线上依次的模块名： 0:未配置  1:CIV512  2:CIV521  3:CMM10X  4:DEE021  5:F6
        '''
        if self.board_1_modules_ios is not None:
            # 解析主底板上的各模块以及模块上的IO配置信息
            #  board_1_modules_count格式： {'CDM163': 2, 'CTO163': 1}
            board_1_modules_count = {}
            for idx in range(len(self.board_1_modules_ios)):
                module = self.board_1_modules_ios[idx][0].upper()
                if module != '':
                    # IO位置的偏移量
                    board_1_io_pos_offset = {'DI': 0, 'DO': 0, 'AI': 0, 'AO': 0, 'TI': 0, 'TO': 0}
                    if module not in board_1_modules_count:
                        board_1_modules_count[module] = 1
                    else:
                        board_1_modules_count[module] += 1
                    # 根据不同的模块，对应不同的起始位置，比如第一块CTO163，DO从41开始
                    if self.imm_type != 'VE2':
                        if module == 'CTO163':
                            if board_1_modules_count[module] == 1:
                                board_1_io_pos_offset['DO'] = 41 - 1
                                self.module_config_info['3'][idx] = 2
                            elif board_1_modules_count[module] == 2:
                                board_1_io_pos_offset['DO'] = 57 - 1
                                self.module_config_info['3'][idx] = 3
                            else:
                                print('Error: 标准程序CMM102主底板支持至多2块CTO163')
                                self.status = -2
                                break
                        if module == 'CDI163':
                            if board_1_modules_count[module] == 1:
                                board_1_io_pos_offset['DI'] = 57 - 1
                                self.module_config_info['3'][idx] = 1
                            else:
                                print('Error: 标准程序CMM102主底板支持至多1块CDI163')
                                self.status = -2
                                break
                        if module == 'CDM163':
                            if board_1_modules_count[module] == 1:
                                board_1_io_pos_offset['DI'] = 81 - 1
                                board_1_io_pos_offset['DO'] = 81 - 1
                                self.module_config_info['3'][idx] = 7
                            elif board_1_modules_count[module] == 2:
                                board_1_io_pos_offset['DI'] = 89 - 1
                                board_1_io_pos_offset['DO'] = 89 - 1
                                self.module_config_info['3'][idx] = 8
                            elif board_1_modules_count[module] == 3:
                                board_1_io_pos_offset['DI'] = 97 - 1
                                board_1_io_pos_offset['DO'] = 97 - 1
                                self.module_config_info['3'][idx] = 9
                            elif board_1_modules_count[module] == 4:
                                board_1_io_pos_offset['DI'] = 105 - 1
                                board_1_io_pos_offset['DO'] = 105 - 1
                                self.module_config_info['3'][idx] = 10
                            else:
                                print('Error: 标准程序CMM102主底板只支持至多4块CDM163')
                                self.status = -2
                                break
                        if module == 'CIO021':
                            if board_1_modules_count[module] == 1:
                                board_1_io_pos_offset['DI'] = 73 - 1
                                board_1_io_pos_offset['DO'] = 73 - 1
                                board_1_io_pos_offset['AI'] = 5 - 1
                                self.module_config_info['3'][idx] = 12
                            else:
                                print('Error: 标准程序CMM102主底板只支持至多1块CIO021')
                                self.status = -2
                                break
                        if module == 'CIO011':
                            if board_1_modules_count[module] == 1:
                                board_1_io_pos_offset['DI'] = 113 - 1
                                board_1_io_pos_offset['DO'] = 129 - 1
                                board_1_io_pos_offset['AI'] = 3 - 1
                                self.module_config_info['3'][idx] = 4
                            else:
                                print('Error: 标准程序CMM102主底板只支持至多1块CIO011')
                                self.status = -2
                                break
                        if module == 'CAI888':
                            if board_1_modules_count[module] == 1:
                                self.module_config_info['3'][idx] = 5
                            elif board_1_modules_count[module] == 2:
                                self.module_config_info['3'][idx] = 6
                            elif board_1_modules_count[module] == 2:
                                self.module_config_info['3'][idx] = 13
                            else:
                                print('Error: 标准程序CMM102主底板只支持3块CAI888')
                    else:
                        if module == 'CTO163':
                            if board_1_modules_count[module] == 1:
                                board_1_io_pos_offset['DO'] = 49 - 1
                                self.module_config_info['1'][0] = 4
                            else:
                                print('Error: 标准程序CIPC主底板支持至多1块CTO163')
                                self.status = -2
                                break
                        if module == 'CDI163':
                            if board_1_modules_count[module] == 1:
                                board_1_io_pos_offset['DI'] = 57 - 1
                                self.module_config_info['1'][0] = 5
                            else:
                                print('Error: 标准程序CIPC主底板支持至多1块CDI163')
                                self.status = -2
                                break
                        if module == 'CDM163':
                            if board_1_modules_count[module] == 1:
                                board_1_io_pos_offset['DI'] = 73 - 1
                                board_1_io_pos_offset['DO'] = 41 - 1
                                self.module_config_info['1'][0] = 3
                            else:
                                print('Error: 标准程序CIPC主底板只支持至多1块CDM163')
                                self.status = -2
                                break
                        if module == 'CIO011' or module == 'CIO021':
                            # 标准程序CIPC主底板只有CIO011
                            if board_1_modules_count[module] == 1:
                                board_1_io_pos_offset['DI'] = 81 - 1
                                board_1_io_pos_offset['DO'] = 65 - 1
                                self.module_config_info['1'][0] = 6
                            else:
                                print('Error: 标准程序CIPC主底板只支持至多1块CIO011')
                                self.status = -2
                                break
                        if module == 'CAI888':
                            # 标准程序只支持3块CAI888
                            if board_1_modules_count[module] == 1:
                                self.module_config_info['1'][0] = 2
                            else:
                                print('Error: 标准程序CIPC主底板只支持1块CAI888')

                    for key, value in self.board_1_modules_ios[idx][1].items():
                        io_type = key[:2].upper()
                        io_seq = int(value)
                        io_pos = int(key[2:]) + board_1_io_pos_offset[io_type]
                        if io_seq in self.io_config_info[io_type]:
                            if io_type != 'TI' and io_type != 'TO':
                                # 同样的IO已经配置过了，不允许重复配置
                                self.status = -3
                        self.io_config_info[io_type][io_seq] = io_pos
                        self.io_reset_info[io_type].add(io_pos)

        if self.board_2_modules_ios is not None and len(self.board_2_modules_ios) > 0:
            board_2_modules_count = {}
            # 去掉扩展底板一的Varan连接模块
            board_2_normal_modules_ios = self.board_2_modules_ios[1:]
            for idx in range(len(board_2_normal_modules_ios)):
                module = board_2_normal_modules_ios[idx][0].upper()
                # 非VE2机的主底板扩展槽内容检测
                if module != '':
                    # IO位置的偏移量
                    board_2_io_pos_offset = {'DI': 0, 'DO': 0, 'AI': 0, 'AO': 0, 'TI': 0, 'TO': 0}
                    if module not in board_2_modules_count:
                        board_2_modules_count[module] = 1
                    else:
                        board_2_modules_count[module] += 1
                    # 根据不同的模块，对应不同的起始位置，比如第一块CTO163，DO从41开始
                    if self.imm_type != 'VE2':
                        if module == 'CTO163':
                            if board_2_modules_count[module] == 1:
                                board_2_io_pos_offset['DO'] = 153 - 1
                                self.module_config_info['4'][idx] = 2
                            elif board_2_modules_count[module] == 2:
                                board_2_io_pos_offset['DO'] = 169 - 1
                                self.module_config_info['4'][idx] = 3
                            else:
                                print('Error: 标准程序CMM102扩展底板一支持至多2块CTO163')
                                self.status = -2
                                break
                        if module == 'CDI163':
                            if board_2_modules_count[module] == 1:
                                board_2_io_pos_offset['DI'] = 169 - 1
                                self.module_config_info['4'][idx] = 1
                            elif board_2_modules_count[module] == 2:
                                board_2_io_pos_offset['DI'] = 217 - 1
                                self.module_config_info['4'][idx] = 14
                            else:
                                print('Error: 标准程序CMM102扩展底板一支持至多2块CDI163')
                                self.status = -2
                                break
                        if module == 'CDM163':
                            if board_2_modules_count[module] == 1:
                                board_2_io_pos_offset['DI'] = 185 - 1
                                board_2_io_pos_offset['DO'] = 185 - 1
                                self.module_config_info['4'][idx] = 4
                            elif board_2_modules_count[module] == 2:
                                board_2_io_pos_offset['DI'] = 209 - 1
                                board_2_io_pos_offset['DO'] = 209 - 1
                                self.module_config_info['4'][idx] = 13
                            else:
                                print('Error: 标注程序CMM102扩展底板一只支持至多2块CDM163')
                                self.status = -2
                                break
                        if module == 'CIO021':
                            if board_2_modules_count[module] == 1:
                                board_2_io_pos_offset['DI'] = 193 - 1
                                board_2_io_pos_offset['DO'] = 193 - 1
                                self.module_config_info['4'][idx] = 11
                            else:
                                print('Error: 标注程序CMM102扩展底板一只支持至多1块CIO021')
                                self.status = -2
                                break
                        if module == 'CIO011':
                            if board_2_modules_count[module] == 1:
                                board_2_io_pos_offset['DI'] = 201 - 1
                                board_2_io_pos_offset['DO'] = 201 - 1
                                self.module_config_info['4'][idx] = 12
                            else:
                                print('Error: 标注程序CMM102扩展底板一只支持至多1块CIO011')
                                self.status = -2
                                break
                        if module == 'CAI888':
                            if board_2_modules_count[module] == 1:
                                self.module_config_info['4'][idx] = 5
                            elif board_2_modules_count[module] == 2:
                                self.module_config_info['4'][idx] = 6
                            elif board_2_modules_count[module] == 3:
                                self.module_config_info['4'][idx] = 7
                            elif board_2_modules_count[module] == 4:
                                self.module_config_info['4'][idx] = 8
                            elif board_2_modules_count[module] == 5:
                                self.module_config_info['4'][idx] = 9
                            else:
                                print('Error: 标准程序CMM102扩展底板一只支持5块CAI888')
                                self.status = -2
                    else:
                        if module == 'CTO163':
                            if board_2_modules_count[module] == 1:
                                board_2_io_pos_offset['DO'] = 73 - 1
                                self.module_config_info['2'][idx] = 3
                            elif board_2_modules_count[module] == 2:
                                board_2_io_pos_offset['DO'] = 89 - 1
                                self.module_config_info['2'][idx] = 4
                            else:
                                print('Error: 标准程序CIPC扩展底板一支持至多2块CTO163')
                                self.status = -2
                                break
                        if module == 'CDI163':
                            if board_2_modules_count[module] == 1:
                                board_2_io_pos_offset['DI'] = 89 - 1
                                self.module_config_info['2'][idx] = 1
                            elif board_2_modules_count[module] == 2:
                                board_2_io_pos_offset['DI'] = 105 - 1
                                self.module_config_info['2'][idx] = 2
                            else:
                                print('Error: 标准程序CIPC扩展底板一支持至多2块CDI163')
                                self.status = -2
                                break
                        if module == 'CDM163':
                            if board_2_modules_count[module] == 1:
                                board_2_io_pos_offset['DI'] = 121 - 1
                                board_2_io_pos_offset['DO'] = 105 - 1
                                self.module_config_info['2'][idx] = 5
                            elif board_2_modules_count[module] == 2:
                                board_2_io_pos_offset['DI'] = 137 - 1
                                board_2_io_pos_offset['DO'] = 121 - 1
                                self.module_config_info['2'][idx] = 13
                            elif board_2_modules_count[module] == 3:
                                board_2_io_pos_offset['DI'] = 145 - 1
                                board_2_io_pos_offset['DO'] = 129 - 1
                                self.module_config_info['2'][idx] = 14
                            else:
                                print('Error: 标注程序CIPC扩展底板一只支持至多3块CDM163')
                                self.status = -2
                                break
                        if module == 'CIO011' or module == 'CIO021':
                            # 标准程序CIPC主底板只有CIO011
                            if board_2_modules_count[module] == 1:
                                board_2_io_pos_offset['DI'] = 129 - 1
                                board_2_io_pos_offset['DO'] = 113 - 1
                                self.module_config_info['2'][idx] = 7
                            elif board_2_modules_count[module] == 2:
                                board_2_io_pos_offset['DI'] = 153 - 1
                                board_2_io_pos_offset['DO'] = 137 - 1
                                self.module_config_info['2'][idx] = 15
                            elif board_2_modules_count[module] == 3:
                                board_2_io_pos_offset['DI'] = 161 - 1
                                board_2_io_pos_offset['DO'] = 145 - 1
                                self.module_config_info['2'][idx] = 16
                            else:
                                print('Error: 标准程序CIPC扩展底板一只支持至多3块CIO011')
                                self.status = -2
                                break
                        if module == 'CAI888':
                            if board_2_modules_count[module] == 1:
                                self.module_config_info['2'][idx] = 8
                            elif board_2_modules_count[module] == 2:
                                self.module_config_info['2'][idx] = 9
                            elif board_2_modules_count[module] == 3:
                                self.module_config_info['2'][idx] = 10
                            elif board_2_modules_count[module] == 4:
                                self.module_config_info['2'][idx] = 11
                            elif board_2_modules_count[module] == 5:
                                self.module_config_info['2'][idx] = 12
                            else:
                                print('Error: 标准程序CMM102扩展底板一只支持5块CAI888')
                                self.status = -2
                        pass

                    for key, value in board_2_normal_modules_ios[idx][1].items():
                        io_type = key[:2].upper()
                        io_seq = int(value)
                        io_pos = int(key[2:]) + board_2_io_pos_offset[io_type]
                        if io_seq in self.io_config_info[io_type]:
                            if io_type != 'TI' and io_type != 'TO':
                                # 同样的IO已经配置过了，不允许重复配置
                                self.status = -3
                        self.io_config_info[io_type][io_seq] = io_pos
                        self.io_reset_info[io_type].add(io_pos)

        # 能耗模块DEE是否启用
        if self.dee:
            if self.imm_type != 'VE2':
                self.varan_config_info = [3, 4, 5]
            else:
                self.varan_config_info = [0, 0, 4, 5]
        # Varan连接模块
        if self.board_2_modules_ios is not None and len(self.board_2_modules_ios) > 0:
            varan_conn_module = self.board_2_modules_ios[0][0]
            if varan_conn_module.upper() == 'CIV512':
                if self.varan_module_pos == 0:
                    self.varan_config_info.append(1)
                else:
                    self.varan_config_info.insert(1, 1)
            else:
                if varan_conn_module.upper() == 'CIV521':
                    if self.varan_module_pos == 0:
                        self.varan_config_info.append(2)
                    else:
                        self.varan_config_info.insert(1, 2)

        # 不要去尝试配置模块上的TI和TO点位，容易出错！
        self.io_config_info['TI'] = {}
        self.io_config_info['TO'] = {}

        if self.main_board_modified_io is not None:
            # 解析主底板上的IO配置信息
            # main_board_modified_io = {'DI7': 111, 'AO36': 45}
            for k, v in self.main_board_modified_io.items():
                io_type = k[:2]
                io_seq = v
                io_pos = int(k[2:])
                self.io_reset_info[io_type].add(io_pos)
                if io_seq == 0:
                    continue
                if io_type == 'AI' and self.imm_type.upper() != 'VE2':
                    # 还原CMM103的AI点位置，默认底板的AI位置是1,2,9,10,16,17
                    if io_pos in [1, 2]:
                        self.io_config_info[io_type][io_seq] = io_pos
                    if io_pos in [3, 4]:
                        self.io_config_info[io_type][io_seq] = io_pos + 6
                    if io_pos in [5, 6]:
                        self.io_config_info[io_type][io_seq] = io_pos + 11
                else:
                    self.io_config_info[io_type][io_seq] = io_pos

    def createFile(self):
        '''
            根据IO配置点，修改硬件配置文件
            :return     >=0    文件的修改行数
                        -1      标准程序不支持的模块配置
                        -2      文件复制时候发生错误
        '''
        if self.status == 0:
            self._getConfigInfo()
        if self.status < 0:
            print("当前状态不允许生成硬件配置文件, status:", self.status)
            return -1
        if self.std_file_path != '':
            shutil.copyfile(self.std_file_path, self.dst_file_path)
        else:
            print("未找到标准硬件配置文件")
        if not os.path.isfile(self.dst_file_path):
            print("目标配置文件不存在，可能复制文件过程中发生了错误")
            return -2
        if self.io_config_info is None and self.module_config_info is None:
            return 0
        with open(self.dst_file_path, 'r+') as fp:
            row_need_modified = 0
            lines = fp.readlines()
            re_exp = re.compile(r',\d+,,')
            # 备份标准硬件配置文件，用来后面的修改行数比较
            lines_duplicated = lines.copy()
            for line in lines:
                parsed_result = self._parseLineInfo(line)
                if parsed_result is not None:
                    # 定位IO行
                    if parsed_result['type'] == 'IO':
                        io_type = str(parsed_result['name'])
                        io_seq = parsed_result['seq']
                        io_pos = parsed_result['pos']
                        if io_pos in self.io_reset_info[io_type]:
                            lines[row_need_modified] = re_exp.sub(',0,,', line)
                        if io_seq in self.io_config_info[io_type]:
                            lines[row_need_modified] = re_exp.sub(',' + str(self.io_config_info[io_type][io_seq]) + ',,', line)
                    # 定位Module行
                    if parsed_result['type'] == 'Module':
                        board = str(parsed_result['name'])
                        slot_seq = int(parsed_result['seq'])
                        # module_idx = parsed_result['pos']
                        if board != '1' and board in self.module_config_info and slot_seq < len(self.module_config_info[board]):
                            #   module_config_info = {'3': [1, 3, 0, 0], '4': [5, 3, 0]}
                            lines[row_need_modified] = re_exp.sub(',' + str(self.module_config_info[board][slot_seq]) + ',,', line)
                        if board == '1' and slot_seq == 7 and self.imm_type == 'VE2':
                            lines[row_need_modified] = re_exp.sub(',' + str(self.module_config_info[board][0]) + ',,', line)
                    # 定位Varan连接模块行
                    if parsed_result['type'] == 'Varan':
                        varan_num = str(parsed_result['name'])
                        varan_node = int(parsed_result['seq'])
                        # varan_module_idx = parsed_result['pos']
                        if varan_num == '1' and varan_node <= len(self.varan_config_info):
                            lines[row_need_modified] = re_exp.sub(',' + str(self.varan_config_info[varan_node - 1]) + ',,', line)
                row_need_modified += 1
            fp.seek(0)
            fp.truncate()
            # 计算硬件配置文件的改动行数
            lines_modified = set(lines).difference(set(lines_duplicated))
            lines_modified_count = len(lines_modified)
            for line in lines:
                fp.write(line)
        if lines_modified_count > 0:
            # 若硬件配置文件发生了更改，需要在文件名中体现出更改的行数
            temp = os.path.splitext(self.dst_file_path)
            if len(temp) == 2:
                new_dst_file_path = temp[0] + 'm' + str(lines_modified_count) + temp[1]
                os.rename(self.dst_file_path, new_dst_file_path)
                self.dst_file_path = new_dst_file_path
        return lines_modified_count

    def _parseLineInfo(self, line):
        '''
            解析硬件配置文件中的每一行的信息
            :return: {type: 'IO', name: 'DI', seq: 73, pos: 0}    第73号DI点，配在0号位置，即未配置
                      {type: 'Module', name: '3', seq: 0, pos: 0}  第3号底板(ZE 2S机的主底板)，第1个插槽，配0号模块，即未配置
                        底板说明： name: '1'     CIPC主底板
                                        '2'     CIPC的扩展底板一
                                        '3'     CCP621 CMM102 主底板
                                        '4'     CCP621 CMM102 扩展底板一
                      {type: 'Varan', name: '1', seq: 3, pos: 1}   第1号Varan线，第3个节点，配0号模块，即未配置
                      None             这一行既不是IO点配置行，也不是模块配置行，也不是Varan配置行
        '''
        ret_info = {'type': '', 'name': '', 'seq': '', 'pos': ''}
        # 尝试匹配IO点，格式如下：
        # Digtal_In_SWC1.Func_32,40,,{512},{3},255,
        result = re.search(r'(\w+).Func_(\d+),(\d+),,', line)
        if result:
            # 定位IO行
            ret_info['type'] = 'IO'
            title = result.group(1)
            seq = result.group(2)
            pos = result.group(3)
            if title == 'Digtal_In_SWC1':
                ret_info['name'] = 'DI'
            elif title == 'Digtal_Out_SWC1':
                ret_info['name'] = 'DO'
            elif title == 'Analog_IO_SWC1':
                if seq.startswith('0') and seq.endswith('0'):
                    ret_info['name'] = 'AO'
                    seq = seq[:-1]
                else:
                    ret_info['name'] = 'AI'
            elif title == 'Analog_IO_SWC2':
                if seq.endswith('0') and seq.startswith('0'):
                    ret_info['name'] = 'TO'
                    seq = seq[:-1]
                else:
                    ret_info['name'] = 'TI'
            ret_info['seq'] = int(seq)
            ret_info['pos'] = int(pos)
            return ret_info
        # 尝试匹配模块，格式如下
        # HardwareAddressesConfig3.Plug1,0,,{512},{3},255,
        result = re.search(r'HardwareAddressesConfig(\d+)\.Plug(\d+),(\d+),,', line)
        if result:
            ret_info['type'] = 'Module'
            ret_info['name'] = result.group(1)
            ret_info['seq'] = int(result.group(2))
            ret_info['pos'] = int(result.group(3))
            return ret_info
        # 尝试匹配Varan接线模块，格式如下
        # ConfigFileProducer1.sShowVaran1Node1,3,,{512},{1},255,
        result = re.search(r'sShowVaran(\d+)Node(\d+),(\d+),,', line)
        if result:
            ret_info['type'] = 'Varan'
            ret_info['name'] = result.group(1)
            ret_info['seq'] = int(result.group(2))
            ret_info['pos'] = int(result.group(3))
            return ret_info
        return None

    def getStdIoInfo(self):
        '''

        :return: 默认底板/模块系统上的IO配置信息，格式如：
            {'DI': [9, 10, 0, ...], 'DO': [], ...}
            0代表该位置未配置IO
        '''
        std_io_config = {'DI': [0 for i in range(self.std_io_num['DI'])],
                         'DO': [0 for i in range(self.std_io_num['DO'])],
                         'AI': [0 for i in range(self.std_io_num['AI'])],
                         'AO': [0 for i in range(self.std_io_num['AO'])],
                         'TI': [0 for i in range(self.std_io_num['TI'])],
                         'TO': [0 for i in range(self.std_io_num['TO'])]}

        if self.std_file_path != '':
            with open(self.std_file_path, 'r') as fp:
                lines = fp.readlines()
                for line in lines:
                    parsed_result = self._parseLineInfo(line)
                    if parsed_result is not None:
                        if parsed_result['type'] == 'IO':
                            io_type = parsed_result['name']
                            io_seq = parsed_result['seq']
                            io_pos = parsed_result['pos']
                            if io_pos != 0:
                                if io_type == 'AI' and self.imm_type != 'VE2':
                                    # CMM103底板AI点居然是1,2,9,10,16,17 -.-!
                                    if io_pos in [1, 2]:
                                        std_io_config['AI'][io_pos - 1] = io_seq
                                    if io_pos in [9, 10]:
                                        std_io_config['AI'][io_pos - 7] = io_seq
                                    if io_pos in [16, 17]:
                                        std_io_config['AI'][io_pos - 12] = io_seq
                                else:
                                    if io_pos <= self.std_io_num[io_type]:
                                        std_io_config[io_type][io_pos - 1] = io_seq

        return std_io_config


class FcfFileMaker:
    def __init__(self, imm_type, ce_standard=False, functions=None,
                 std_file_dir=STD_FCF_FILE_DIR,
                 dst_file_dir=CACHE_FILE_DIR,
                 func_output1=0, func_output2=0):
        '''
            functions: {'injSig': True, 'chargeSig': False, 'internalHotrunnerNum': 0, 'dee': False}
        '''
        self.functions = functions
        self.std_file_path = ''
        self.dst_file_path = ''
        for file_name in os.listdir(os.path.join(std_file_dir, imm_type)):
            if ce_standard:
                if 'CE' in file_name:
                    self.std_file_path = os.path.join(std_file_dir, imm_type, file_name)
                    self.dst_file_path = os.path.join(dst_file_dir, file_name)
            else:
                if 'CE' not in file_name:
                    self.std_file_path = os.path.join(std_file_dir, imm_type, file_name)
                    self.dst_file_path = os.path.join(dst_file_dir, file_name)
        self.func_output1 = func_output1
        self.func_output2 = func_output2

    def createFile(self):
        if not os.path.isfile(self.std_file_path):
            print('没有找到标准功能配置文件')
            return -1
        shutil.copyfile(self.std_file_path, self.dst_file_path)
        if not os.path.isfile(self.dst_file_path):
            print("功能配置文件复制过程中发生了错误")
            return -2
        with open(self.dst_file_path, 'r+') as fp:
            row_need_modified = 0
            lines = fp.readlines()
            for line in lines:
                # TODO: 打开相应的功能
                # if 'injSig' in self.functions and self.functions['injSig'] and \
                #         re.search(r"SelectOutput1\.ClassSvr", line):
                #     lines[row_need_modified] = re.sub(r",\d+,,", r",1,,", line)
                # if 'chargeSig' in self.functions and  self.functions['chargeSig'] and \
                #         re.search(r"SelectOutput2\.ClassSvr", line):
                #     lines[row_need_modified] = re.sub(r",\d+,,", r",2,,", line)
                if self.func_output1 != 0 and re.search(r"SelectOutput1\.ClassSvr", line):
                    lines[row_need_modified] = re.sub(r",\d+,,", r"," + str(self.func_output1) + ",,", line)
                if self.func_output2 != 0 and re.search(r"SelectOutput2\.ClassSvr", line):
                    lines[row_need_modified] = re.sub(r",\d+,,", r"," + str(self.func_output2) + ",,", line)
                if 'internalHotrunnerNum' in self.functions and int(self.functions['internalHotrunnerNum']) > 0 and \
                        re.search(r"MoldHeating\.sMoldHeatingSelection", line):
                    lines[row_need_modified] = re.sub(r",\d+,,", "," + str(self.functions['internalHotrunnerNum']) + ",,", line)
                if 'dee' in self.functions and self.functions['dee'] and \
                        re.search(r'FileEvaluation1\.DEE_Enable', line):
                    lines[row_need_modified] = re.sub(r",\d+,,", r",1,,", line)
                if 'valve' in self.functions and self.functions['valve'] and \
                        re.search(r"OptionalFunction\.sVolveGate", line):
                    lines[row_need_modified] = re.sub(r",\d+,,", r",1,,", line)
                if 'air' in self.functions and self.functions['air'] and \
                        re.search(r"OptionalFunction\.sAirblowVisible", line):
                    lines[row_need_modified] = re.sub(r",\d+,,", r",1,,", line)
                if 'core' in self.functions and self.functions['core'] and \
                        re.search(r"OptionalFunction\.sCoreVisible", line):
                    lines[row_need_modified] = re.sub(r",\d+,,", r",1,,", line)
                if 'progio' in self.functions and self.functions['progio'] and \
                        re.search(r"OptionalFunction\.sProgrammableIO", line):
                    lines[row_need_modified] = re.sub(r",\d+,,", r",1,,", line)

                row_need_modified += 1
            fp.seek(0)
            fp.truncate()
            for line in lines:
                fp.write(line)
        return 0


class SysFileMaker:
    def __init__(self, ce_standard=False, clamp_force=40,
                 std_file_dir=STD_SYS_FILE_DIR,
                 dst_file_dir=CACHE_FILE_DIR):
        self.std_file_path = ''
        self.dst_file_path = ''
        for file_name in os.listdir(std_file_dir):
            if ce_standard and 'CE' in file_name:
                if int(clamp_force) <= 5500 and '550' in file_name:
                    self.std_file_path = os.path.join(std_file_dir, file_name)
                    self.dst_file_path = os.path.join(dst_file_dir, file_name)
                if int(clamp_force) > 5500 and '650' in file_name:
                    self.std_file_path = os.path.join(std_file_dir, file_name)
                    self.dst_file_path = os.path.join(dst_file_dir, file_name)
            if not ce_standard and 'CE' not in file_name:
                if int(clamp_force) <= 5500 and '550' in file_name:
                    self.std_file_path = os.path.join(std_file_dir, file_name)
                    self.dst_file_path = os.path.join(dst_file_dir, file_name)
                if int(clamp_force) > 5500 and '650' in file_name:
                    self.std_file_path = os.path.join(std_file_dir, file_name)
                    self.dst_file_path = os.path.join(dst_file_dir, file_name)

    def createFile(self):
        if not os.path.isfile(self.std_file_path):
            print('未找到标准系统文件')
            return -1
        shutil.copyfile(self.std_file_path, self.dst_file_path)
        if not os.path.isfile(self.dst_file_path):
            print('复制系统文件过程中发生了错误')
            return -2
        return 0


class SafetyFileMaker:
    def __init__(self, nor_pilz=None, e73_pilz=None,
                 std_nor_pilz_dir=NOR_SAFETY_RELAY_FILE_DIR,
                 std_e73_pilz_dir=E73_SAFETY_RELAY_FILE_DIR,
                 dst_file_dir=CACHE_FILE_DIR):
        self.std_nor_pilz_path = None
        self.dst_nor_pilz_path = None
        if nor_pilz is not None:
            self.std_nor_pilz_path = os.path.join(std_nor_pilz_dir, nor_pilz)
            self.dst_nor_pilz_path = os.path.join(dst_file_dir, nor_pilz)

        self.std_e73_pilz_path = None
        self.dst_e73_pilz_path = None
        if e73_pilz is not None:
            self.std_e73_pilz_path = os.path.join(std_e73_pilz_dir, e73_pilz)
            self.dst_e73_pilz_path = os.path.join(dst_file_dir, e73_pilz)

    def createFile(self):
        if self.std_nor_pilz_path is not None and os.path.isfile(self.std_nor_pilz_path):
            shutil.copyfile(self.std_nor_pilz_path, self.dst_nor_pilz_path)
            if not os.path.isfile(self.dst_nor_pilz_path):
                print('复制普通安全继电器文件失败')
                return -1
        if self.std_e73_pilz_path is not None and os.path.isfile(self.std_e73_pilz_path):
            shutil.copyfile(self.std_e73_pilz_path, self.dst_e73_pilz_path)
            if not os.path.isfile(self.dst_e73_pilz_path):
                print('复制E73安全继电器文件失败')
                return -2
        return 0



def createZip(file_dir, dst_zip_path=''):
    '''
        将某个文件夹打包成zip文件，最后返回zip文件路径
        file_dir:       文件夹的目录名
        dst_zip_path:   *.zip文件的路径
    '''
    if dst_zip_path == '':
        dst_zip_path = file_dir.strip(r' \/') + '.zip'
    if os.path.isfile(dst_zip_path):
        os.remove(dst_zip_path)
    fp = zipfile.ZipFile(dst_zip_path, 'w')
    for file_name in os.listdir(file_dir):
        file_path = os.path.join(file_dir, file_name)
        fp.write(file_path, file_name, zipfile.ZIP_DEFLATED)
    fp.close()
    return dst_zip_path


if __name__ == '__main__':
    createZip(r'F:\MyProj\app\static\cache')
