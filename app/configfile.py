import os
import shutil
import re


class HardwareConfigFile:
    def __init__(self, imm_type, io_config_info=None, ce_standard=False,
                 std_file_dir='./app/libfiles/配置文件/硬件配置文件/',
                 dst_file_dir='./app/static/cache/'):
        '''
            imm_type：格式如：ZEs/ZE/VE2s/VE2
            dst_file_dir: 默认为./app/static/cache/，为了迎合网页端的文件下载接口，文件需要放在.static/目录下
            io_config_info：{'DI':{41: 41, 73: 81}, 'DO': {}, 'AI': {}, ... }  key是IO的序号，value是IO的位置
        '''
        self.imm_type = imm_type.upper()
        self.io_config_info = io_config_info

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
        if self.io_config_info is None:
            return 0
        with open(self.dst_file_path, 'r+') as fp:
            row_need_modified = 0
            lines = fp.readlines()
            for line in lines:
                parsed_result = self._parseLineInfo(line)
                if parsed_result is not None:
                    io_type = parsed_result['name']
                    io_seq = parsed_result['seq']
                    if io_seq in self.io_config_info[io_type]:
                        re_exp = re.compile(r',\d+,,')
                        lines[row_need_modified] = re_exp.sub(',' + str(self.io_config_info[io_type][io_seq]) + ',,', line)
                row_need_modified += 1
            fp.seek(0)
            fp.truncate()
            for line in lines:
                fp.write(line)
        return 0

    def _parseLineInfo(self, line):
        '''
            解析硬件配置文件中的每一行的信息
            :return: {name: 'DI', seq: 73, pos: 0}
            TODO: 需要解析模块信息，替换模块
        '''
        ret_info = {'name': '', 'seq': '', 'pos': ''}
        result = re.search(r'(\w+).Func_(\d+),(\d+),', line)
        if not result:
            return None
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
