import os
import shutil
import re


class HardwareConfigFile:
    def __init__(self, imm_type, ce_standard=False,
                 io_config_info=None,
                 module_config_info=None,
                 varan_config_info=None,
                 std_file_dir='./app/libfiles/配置文件/硬件配置文件/',
                 dst_file_dir='./app/static/cache/'):
        '''
            imm_type：格式如：ZEs/ZE/VE2s/VE2
            dst_file_dir: 默认为./app/static/cache/，为了迎合网页端的文件下载接口，文件需要放在.static/目录下
            io_config_info：{'DI':{41: 41, 73: 81}, 'DO': {}, 'AI': {}, ... }  key是IO的序号，value是IO的位置
            module_config_info: {'3': [1, 3, 0, 0], '4': [5, 3, 0]}     key是board的序号，value是底板上的模块序号数，这里不显示Varan模块
            varan_config_info: [3, 5, 1]    List内的值依次是Varan1总线节点的模块序号
        '''
        self.imm_type = imm_type.upper()
        self.io_config_info = io_config_info
        self.module_config_info = module_config_info
        self.varan_ocnfig_info = varan_config_info

        if imm_type.endswith('S'):
            self.ce_standard = ce_standard
        else:
            self.ce_standard = False

        # 根据机型以及安全标准确定 “标准硬件配置” 和 修改后的 “特殊硬件配置” 文件路径
        self.std_file_path = ''
        self.dst_file_path = ''
        print(os.getcwd())
        print(self.std_file_path)
        for file_name in os.listdir(os.path.join(std_file_dir, self.imm_type)):
            if self.ce_standard:
                if 'BCD' and self.imm_type in file_name.upper():
                    if self.std_file_path == '':
                        self.std_file_path = os.path.join(std_file_dir, self.imm_type, file_name)
                        self.dst_file_path = os.path.join(dst_file_dir, file_name)
                    else:
                        print("找到了好几份符合标准的硬件配置文件")
                        break
            else:
                if self.imm_type and 'BCD' not in file_name.upper():
                    if self.std_file_path == '':
                        self.std_file_path = os.path.join(std_file_dir, self.imm_type, file_name)
                        self.dst_file_path = os.path.join(dst_file_dir, file_name)
                    else:
                        print("找到了好几份符合标准的硬件配置文件")
                        break
        if self.std_file_path != '':
            shutil.copyfile(self.std_file_path, self.dst_file_path)
        else:
            print("未找到标准硬件配置文件")

    def getFilePath(self):
        '''
            获取修改完成的硬件配置文件路径
            （为网页端提供下载接口，路径以 './static/' 开头）
        '''
        if os.path.isfile(self.dst_file_path):
            # TODO: 尚未修改为./static开头的路径
            return self.dst_file_path

    def modifyDstFile(self):
        '''
            根据IO配置点，修改硬件配置文件
            :return     0       一切顺利
                        -1      文件根本不存在，严重错误
                        -2      文件修改失败
        '''
        if not os.path.isfile(self.dst_file_path):
            print("目标配置文件不存在，可能复制文件过程中发生了错误")
            return -1
        if self.io_config_info is None and self.module_config_info is None:
            return 0
        with open(self.dst_file_path, 'r+') as fp:
            row_need_modified = 0
            lines = fp.readlines()
            for line in lines:
                parsed_result = self._parseLineInfo(line)
                if parsed_result is not None:
                    # 定位IO行
                    if parsed_result['type'] == 'IO':
                        io_type = str(parsed_result['name'])
                        io_seq = int(parsed_result['seq'])
                        # io_pos = parsed_result['pos']
                        if io_seq in self.io_config_info[io_type]:
                            #   io_config_info = {'DI':{41: 41, 73: 81}, 'DO': {}, 'AI': {}, ... }
                            re_exp = re.compile(r',\d+,,')
                            lines[row_need_modified] = re_exp.sub(',' + str(self.io_config_info[io_type][io_seq]) + ',,', line)
                    # 定位Module行
                    if parsed_result['type'] == 'Module':
                        board = str(parsed_result['name'])
                        slot_seq = int(parsed_result['seq'])
                        # module_idx = parsed_result['pos']
                        if board in self.module_config_info and slot_seq < len(self.module_config_info[board]):
                            #   module_config_info = {'3': [1, 3, 0, 0], '4': [5, 3, 0]}
                            re_exp = re.compile(r',\d+,,')
                            lines[row_need_modified] = re_exp.sub(',' + str(self.module_config_info[board][slot_seq]) + ',,', line)
                    # 定位Varan连接模块行
                    if parsed_result['type'] == 'Varan':
                        varan_num = str(parsed_result['name'])
                        varan_node = int(parsed_result['seq'])
                        # varan_module_idx = parsed_result['pos']
                        if varan_num == '1' and varan_node <= len(self.varan_ocnfig_info):
                            re_exp = re.compile(r',\d+,,')
                            lines[row_need_modified] = re_exp.sub(',' + str(self.varan_ocnfig_info[varan_node - 1]) + ',,', line)
                row_need_modified += 1
            fp.seek(0)
            fp.truncate()
            for line in lines:
                fp.write(line)
        return 0

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
                if seq.endswith('0'):
                    ret_info['name'] = 'AO'
                    seq = seq[:-1]
                else:
                    ret_info['name'] = 'AI'
            elif title == 'Analog_IO_SWC2':
                if seq.endswith('0'):
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
