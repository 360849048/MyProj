from app.sqljob import TableManager
from app.exceler import IOFile
from app.pathinfo import *


class IOMaker:
    def __init__(self, imm_type, board_1_modules_ios=None, board_2_modules_ios=None, big=False,
                 evaluation_num=None, production_num=None, type_string=None, customer=None,
                 safety_standard=None, technical_clause=None, dual_inj=False, external_hotrunner_num=0,
                 energy_dee=False, varan_conn_module_pos=0, psg_hotrunner=False):
        '''
            imm_type:           'ZEs', 'ZE', 'VE2', 'VE2s'
            board_1_modules_ios: [['CTO163', {'DO3': OutputID, ...}], ['CDM163', {'DI5': InputID, ...}], ...]
            board_2_modules_ios:    [['CTO163', {'DO3': OutputID, ...}], ['CDM163', {'DI5': InputID, ...}], ...]
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
        self.big = big
        self.evaluation_num = evaluation_num
        self.production_num = production_num
        self.type_string = type_string
        self.customer = customer
        self.safety_standard = safety_standard
        self.technical_clause = technical_clause

        self.dual_inj = dual_inj
        self.energy_dee = energy_dee
        self.psg_hotrunner = psg_hotrunner

        if external_hotrunner_num > 0:
            self.external_hot_runner_cai888_configuration = {
                'TI1': self.t_ti.displayBriefData(1, 'CName', 'EName'),
                'TI2': self.t_ti.displayBriefData(2, 'CName', 'EName'),
                'TI3': self.t_ti.displayBriefData(3, 'CName', 'EName'),
                'TI4': self.t_ti.displayBriefData(4, 'CName', 'EName'),
                'TI5': self.t_ti.displayBriefData(5, 'CName', 'EName'),
                'TI6': self.t_ti.displayBriefData(6, 'CName', 'EName'),
                'TI7': self.t_ti.displayBriefData(7, 'CName', 'EName'),
                'TI8': self.t_ti.displayBriefData(8, 'CName', 'EName'),
                'TO1': self.t_to.displayBriefData(1, 'CName', 'EName'),
                'TO2': self.t_to.displayBriefData(2, 'CName', 'EName'),
                'TO3': self.t_to.displayBriefData(3, 'CName', 'EName'),
                'TO4': self.t_to.displayBriefData(4, 'CName', 'EName'),
                'TO5': self.t_to.displayBriefData(5, 'CName', 'EName'),
                'TO6': self.t_to.displayBriefData(6, 'CName', 'EName'),
                'TO7': self.t_to.displayBriefData(7, 'CName', 'EName'),
                'TO8': self.t_to.displayBriefData(8, 'CName', 'EName')
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

        self.xlsxObj = IOFile(imm_type=self.imm_type,
                              main_board_modules=self.board_1_modules_ios,
                              board_1_modules=self.board_2_modules_ios,
                              big=self.big,
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
                              psg_hotrunner=self.psg_hotrunner)

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

        self.xlsxObj.copyMainBoardModulesInfo()
        self.xlsxObj.copyMainBoardModules()
        self.xlsxObj.copyBoard1ModulesInfo()
        self.xlsxObj.copyBoard1Modules()
        self.xlsxObj.copyExternalHotrunnerInfo()
        self.xlsxObj.copyExternalHotrunnerModule(self.external_hot_runner_cai888_configuration)
        self.xlsxObj.copyEnergyModuleInfo()
        self.xlsxObj.saveAs(path)


if __name__ == '__main__':
    # 功能测试
    iomaker = IOMaker(imm_type='ZEs',
                      board_1_modules_ios=[
                          ['CDM163', {
                              'DI1': '73',
                              'DI2': '74',
                          }],
                          ['CDM163', {
                              'DO1': '73',
                              'DO2': '74',
                          }]
                      ],
                      board_2_modules_ios=[
                          ['civ512', {}],
                          ['cai888', {}],
                      ],
                      big=False
                      )
    iomaker.func1ToInjSignal()
    iomaker.func2ToChargeSignal()
    iomaker.nozzleToValve()
    iomaker.e73Safety()
    iomaker.createFile('./1.xlsx')

