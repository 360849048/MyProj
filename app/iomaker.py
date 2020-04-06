from app.sqljob import TableManager
from app.exceler import IOFile
from app.pathinfo import *


class IOMaker:
    def __init__(self, imm_type, board_1_modules_ios=None, board_2_modules_ios=None,
                 evaluation_num=None, production_num=None, type_string=None, customer=None,
                 safety_standard=None, technical_clause=None, dual_inj=False, external_hotrunner_num=0,
                 energy_dee=False, varan_conn_module_pos=0, psg_hotrunner=False, main_board_modified_io=None):
        '''
            imm_type:           'ZEs', 'ZE', 'VE2', 'VE2s'
            board_1_modules_ios: [['CTO163', {'DO3': OutputID, ...}], ['CDM163', {'DI5': InputID, ...}], ...]
            board_2_modules_ios: [['CTO163', {'DO3': OutputID, ...}], ['CDM163', {'DI5': InputID, ...}], ...]
            main_board_modified_io: {'DI7': InputID, 'DO31': OutputId, ...}
        '''
        self.path_db = IO_INFO_DB_PATH
        self.t_di = TableManager('digital_input', self.path_db)
        self.t_do = TableManager('digital_output', self.path_db)
        self.t_ai = TableManager('Analog_input', self.path_db)
        self.t_ao = TableManager('Analog_output', self.path_db)
        self.t_ti = TableManager('Temperature_input', self.path_db)
        self.t_to = TableManager('Temperature_output', self.path_db)
        self.t_func_list = TableManager('FuncOutput_List', self.path_db)

        self.imm_type = imm_type
        self.board_1_modules_ios = None
        self.board_2_modules_ios = None
        self.evaluation_num = evaluation_num
        self.production_num = production_num
        self.type_string = type_string
        self.customer = customer
        self.safety_standard = safety_standard
        self.technical_clause = technical_clause

        self.dual_inj = dual_inj
        self.energy_dee = energy_dee
        self.psg_hotrunner = psg_hotrunner
        self.main_board_modified_io = None

        if external_hotrunner_num > 0:
            self.external_hot_runner_cai888_configuration = {
                'TI1': ("第一段温度", "Temperature Zone 1"),
                'TI2': ("第二段温度", "Temperature Zone 2"),
                'TI3': ("第三段温度", "Temperature Zone 3"),
                'TI4': ("第四段温度", "Temperature Zone 4"),
                'TI5': ("第五段温度", "Temperature Zone 5"),
                'TI6': ("第六段温度", "Temperature Zone 6"),
                'TI7': ("第七段温度", "Temperature Zone 7"),
                'TI8': ("第八段温度", "Temperature Zone 8"),
                'TO1': ("第一段加热", "Heat Zone 1"),
                'TO2': ("第二段加热", "Heat Zone 2"),
                'TO3': ("第三段加热", "Heat Zone 3"),
                'TO4': ("第四段加热", "Heat Zone 4"),
                'TO5': ("第五段加热", "Heat Zone 5"),
                'TO6': ("第六段加热", "Heat Zone 6"),
                'TO7': ("第七段加热", "Heat Zone 7"),
                'TO8': ("第八段加热", "Heat Zone 8")
            }
        else:
            # 如果没有开启外置热流道，无需专门获取cai888的配点信息
            self.external_hot_runner_cai888_configuration = None
        self.varan_conn_module_pos = varan_conn_module_pos

        # 根据IO的id，在数据库中查找出对应IO的中英文名称
        if board_1_modules_ios is not None:
            self.board_1_modules_ios = board_1_modules_ios.copy()
            for module in self.board_1_modules_ios:
                for io in module[1]:
                    io_id = int(module[1][io])
                    if str(io).upper().startswith('DI'):
                        module[1][io] = self.t_di.displayBriefData(io_id, 'CName', 'EName')
                    if str(io).upper().startswith('DO'):
                        module[1][io] = self.t_do.displayBriefData(io_id, 'CName', 'EName')
                    if str(io).upper().startswith('AI'):
                        module[1][io] = self.t_ai.displayBriefData(io_id, 'CName', 'EName')
                    if str(io).upper().startswith('AO'):
                        module[1][io] = self.t_ao.displayBriefData(io_id, 'CName', 'EName')
                    if str(io).upper().startswith('TI'):
                        module[1][io] = self.t_ti.displayBriefData(io_id, 'CName', 'EName')
                    if str(io).upper().startswith('TO'):
                        module[1][io] = self.t_to.displayBriefData(io_id, 'CName', 'EName')
                # CAI888为空时时默认配置温度和加热点位
                if module[0] == "CAI888" and len(module[1]) == 0:
                    module[1]['TI1'] = ("第一段温度", "Temperature Zone 1")
                    module[1]['TI2'] = ("第二段温度", "Temperature Zone 2")
                    module[1]['TI3'] = ("第三段温度", "Temperature Zone 3")
                    module[1]['TI4'] = ("第四段温度", "Temperature Zone 4")
                    module[1]['TI5'] = ("第五段温度", "Temperature Zone 5")
                    module[1]['TI6'] = ("第六段温度", "Temperature Zone 6")
                    module[1]['TI7'] = ("第七段温度", "Temperature Zone 7")
                    module[1]['TI8'] = ("第八段温度", "Temperature Zone 8")
                    module[1]['TO1'] = ("第一段加热", "Heat Zone 1")
                    module[1]['TO2'] = ("第二段加热", "Heat Zone 2")
                    module[1]['TO3'] = ("第三段加热", "Heat Zone 3")
                    module[1]['TO4'] = ("第四段加热", "Heat Zone 4")
                    module[1]['TO5'] = ("第五段加热", "Heat Zone 5")
                    module[1]['TO6'] = ("第六段加热", "Heat Zone 6")
                    module[1]['TO7'] = ("第七段加热", "Heat Zone 7")
                    module[1]['TO8'] = ("第八段加热", "Heat Zone 8")

        if board_2_modules_ios is not None:
            self.board_2_modules_ios = board_2_modules_ios.copy()
            for module in self.board_2_modules_ios:
                for io in module[1]:
                    io_id = int(module[1][io])
                    if str(io).upper().startswith('DI'):
                        module[1][io] = self.t_di.displayBriefData(io_id, 'CName', 'EName')
                    if str(io).upper().startswith('DO'):
                        module[1][io] = self.t_do.displayBriefData(io_id, 'CName', 'EName')
                    if str(io).upper().startswith('AI'):
                        module[1][io] = self.t_ai.displayBriefData(io_id, 'CName', 'EName')
                    if str(io).upper().startswith('AO'):
                        module[1][io] = self.t_ao.displayBriefData(io_id, 'CName', 'EName')
                    if str(io).upper().startswith('TI'):
                        module[1][io] = self.t_ti.displayBriefData(io_id, 'CName', 'EName')
                    if str(io).upper().startswith('TO'):
                        module[1][io] = self.t_to.displayBriefData(io_id, 'CName', 'EName')
                # CAI888为空时时默认配置温度和加热点位
                if module[0] == "CAI888" and len(module[1]) == 0:
                    module[1]['TI1'] = ("第一段温度", "Temperature Zone 1")
                    module[1]['TI2'] = ("第二段温度", "Temperature Zone 2")
                    module[1]['TI3'] = ("第三段温度", "Temperature Zone 3")
                    module[1]['TI4'] = ("第四段温度", "Temperature Zone 4")
                    module[1]['TI5'] = ("第五段温度", "Temperature Zone 5")
                    module[1]['TI6'] = ("第六段温度", "Temperature Zone 6")
                    module[1]['TI7'] = ("第七段温度", "Temperature Zone 7")
                    module[1]['TI8'] = ("第八段温度", "Temperature Zone 8")
                    module[1]['TO1'] = ("第一段加热", "Heat Zone 1")
                    module[1]['TO2'] = ("第二段加热", "Heat Zone 2")
                    module[1]['TO3'] = ("第三段加热", "Heat Zone 3")
                    module[1]['TO4'] = ("第四段加热", "Heat Zone 4")
                    module[1]['TO5'] = ("第五段加热", "Heat Zone 5")
                    module[1]['TO6'] = ("第六段加热", "Heat Zone 6")
                    module[1]['TO7'] = ("第七段加热", "Heat Zone 7")
                    module[1]['TO8'] = ("第八段加热", "Heat Zone 8")
        if main_board_modified_io is not None:
            self.main_board_modified_io = main_board_modified_io.copy()
            for k, v in self.main_board_modified_io.items():
                #  格式如{'DI7': 110, 'DI8': 111}
                io_type = k[:2]
                if v == 0:
                    self.main_board_modified_io[k] = ('', '')
                else:
                    if io_type == 'DI':
                        self.main_board_modified_io[k] = self.t_di.displayBriefData(v, 'CName', 'EName')
                    if io_type == 'DO':
                        self.main_board_modified_io[k] = self.t_do.displayBriefData(v, 'CName', 'EName')
                    if io_type == 'AI':
                        self.main_board_modified_io[k] = self.t_ai.displayBriefData(v, 'CName', 'EName')
                    if io_type == 'AO':
                        self.main_board_modified_io[k] = self.t_ao.displayBriefData(v, 'CName', 'EName')
                    if io_type == 'TI':
                        self.main_board_modified_io[k] = self.t_ti.displayBriefData(v, 'CName', 'EName')
                    if io_type == 'TO':
                        self.main_board_modified_io[k] = self.t_to.displayBriefData(v, 'CName', 'EName')

        self.xlsxObj = IOFile(imm_type=self.imm_type,
                              main_board_modules=self.board_1_modules_ios,
                              board_1_modules=self.board_2_modules_ios,
                              evaluation_num=self.evaluation_num,
                              production_num=self.production_num,
                              type_string=self.type_string,
                              customer=self.customer,
                              safety_standard=self.safety_standard,
                              technical_clause=self.technical_clause,
                              dual_inj=self.dual_inj,
                              external_hotrunner_num=external_hotrunner_num,
                              energy_dee=self.energy_dee,
                              varan_conn_module_pos=varan_conn_module_pos,
                              psg_hotrunner=self.psg_hotrunner,
                              main_board_modified_io=self.main_board_modified_io)

    # 修改主底板默认点位，每个点位的修改都用一个方法特殊处理
    def func1ToInjSignal(self):
        io_type = 'DO'
        origin_io_name = '功能点1'
        new_io_cname, new_io_ename = ('注射开始', 'Inject Start')
        self.xlsxObj.modifyDefaultIO(io_type=io_type, origin_io_name=origin_io_name,
                                     new_io_cname=new_io_cname, new_io_ename=new_io_ename)

    def func2ToChargeSignal(self):
        io_type = 'DO'
        origin_io_name = '功能点2'
        new_io_cname, new_io_ename = ('储料开始', 'Charge Start')
        self.xlsxObj.modifyDefaultIO(io_type=io_type, origin_io_name=origin_io_name,
                                     new_io_cname=new_io_cname, new_io_ename=new_io_ename)

    def func1Config(self, value):
        io_type = 'DO'
        origin_io_name = '功能点1'
        new_io_cname, new_io_ename = self.t_func_list.displayBriefData(value + 1, 'CName', 'EName')
        self.xlsxObj.modifyDefaultIO(io_type=io_type, origin_io_name=origin_io_name,
                                     new_io_cname=new_io_cname, new_io_ename=new_io_ename)

    def func2Config(self, value):
        io_type = 'DO'
        origin_io_name = '功能点2'
        new_io_cname, new_io_ename = self.t_func_list.displayBriefData(value + 1, 'CName', 'EName')
        self.xlsxObj.modifyDefaultIO(io_type=io_type, origin_io_name=origin_io_name,
                                     new_io_cname=new_io_cname, new_io_ename=new_io_ename)

    def nozzleToValve(self):
        io_type = 'DO'

        io_id1 = 41
        origin_io_name1 = '喷嘴开'
        new_io_cname1, new_io_ename1 = self.t_do.displayBriefData(io_id1, 'CName', 'EName')
        self.xlsxObj.modifyDefaultIO(io_type=io_type, origin_io_name=origin_io_name1,
                                     new_io_cname=new_io_cname1, new_io_ename=new_io_ename1)
        io_id2 = 42
        origin_io_name2 = '喷嘴关'
        new_io_cname2, new_io_ename2 = self.t_do.displayBriefData(io_id2, 'CName', 'EName')
        self.xlsxObj.modifyDefaultIO(io_type=io_type, origin_io_name=origin_io_name2,
                                     new_io_cname=new_io_cname2, new_io_ename=new_io_ename2)

    def e73Safety(self):
        io_type = 'DI'

        io_id1 = 110
        origin_io_name1 = '模内压'
        new_io_cname1, new_io_ename1 = self.t_di.displayBriefData(io_id1, 'CName', 'EName')
        self.xlsxObj.modifyDefaultIO(io_type=io_type, origin_io_name=origin_io_name1,
                                     new_io_cname=new_io_cname1, new_io_ename=new_io_ename1)
        io_id2 = 111
        origin_io_name2 = '开门止'
        new_io_cname2, new_io_ename2 = self.t_di.displayBriefData(io_id2, 'CName', 'EName')
        self.xlsxObj.modifyDefaultIO(io_type=io_type, origin_io_name=origin_io_name2,
                                     new_io_cname=new_io_cname2, new_io_ename=new_io_ename2)

    def moldSlider(self):
        io_type = 'DI'

        io_id1 = 73
        origin_io_name1 = '模内压'
        new_io_cname1, new_io_ename1 = self.t_di.displayBriefData(io_id1, 'CName', 'EName')
        self.xlsxObj.modifyDefaultIO(io_type=io_type, origin_io_name=origin_io_name1,
                                     new_io_cname=new_io_cname1, new_io_ename=new_io_ename1)

    def func1_to_progo1(self):
        io_type = 'DO'

        io_id1 = 73
        origin_io_name1 = '功能点1'
        new_io_cname1, new_io_ename1 = self.t_do.displayBriefData(io_id1, 'CName', 'EName')
        self.xlsxObj.modifyDefaultIO(io_type=io_type, origin_io_name=origin_io_name1,
                                     new_io_cname=new_io_cname1, new_io_ename=new_io_ename1)

    def func2_to_progo2(self):
        io_type = 'DO'

        io_id1 = 74
        origin_io_name1 = '功能点2'
        new_io_cname1, new_io_ename1 = self.t_do.displayBriefData(io_id1, 'CName', 'EName')
        self.xlsxObj.modifyDefaultIO(io_type=io_type, origin_io_name=origin_io_name1,
                                     new_io_cname=new_io_cname1, new_io_ename=new_io_ename1)

    def createFile(self, path):
        self.xlsxObj.modifyImmInfo()
        self.xlsxObj.modifymainBoardIo()
        self.xlsxObj.copyMainBoardModulesInfo()
        self.xlsxObj.copyMainBoardModules()
        self.xlsxObj.copyBoard1ModulesInfo()
        self.xlsxObj.copyBoard1Modules()
        self.xlsxObj.copyExternalHotrunnerInfo()
        self.xlsxObj.copyExternalHotrunnerModule(self.external_hot_runner_cai888_configuration)
        self.xlsxObj.copyEnergyModuleInfo()
        self.xlsxObj.copySE051ModuleInfo()
        self.xlsxObj.saveAs(path)


if __name__ == '__main__':
    # 功能测试
    pass

