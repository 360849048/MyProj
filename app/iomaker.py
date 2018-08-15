from app.sqljob import TableManager
from app.exceler import IOFile


DO_VALVE_1_OPEN = 41
DO_VALVE_2_OPEN = 43
DO_VALVE_3_OPEN = 45
DO_VALVE_4_OPEN = 47
DO_VALVE_5_OPEN = 49
DO_VALVE_6_OPEN = 51
DO_VALVE_7_OPEN = 53
DO_VALVE_8_OPEN = 55

DO_CORE_D_IN = 57
DO_CORE_D_OUT = 58
DO_CORE_E_IN = 59
DO_CORE_E_OUT = 60
DO_CORE_F_IN = 61
DO_CORE_F_OUT = 62

DO_PROGRAMMABLE_1 = 73
DO_PROGRAMMABLE_2 = 74
DO_PROGRAMMABLE_3 = 75
DO_PROGRAMMABLE_4 = 76
DO_PROGRAMMABLE_5 = 77
DO_PROGRAMMABLE_6 = 78

DO_AIR_5 = 81
DO_AIR_6 = 82
DO_AIR_7 = 83
DO_AIR_8 = 84

DO_FLAP_BAD = 107

DO_BAD_PRODUCT_2 = 110

DO_PRESSURE_RELEASE = 120

DO_CORE_2_OUT_END = 121
DO_CORE_2_IN_END = 122


DI_CORE_D_IN_END = 57
DI_CORE_D_OUT_END = 58
DI_CORE_E_IN_END = 59
DI_CORE_E_OUT_END = 60
DI_CORE_F_IN_END = 61
DI_CORE_F_OUT_END = 62

DI_PROGRAMMABLE_1 = 73
DI_PROGRAMMABLE_2 = 74
DI_PROGRAMMABLE_3 = 75
DI_PROGRAMMABLE_4 = 76
DI_PROGRAMMABLE_5 = 77
DI_PROGRAMMABLE_6 = 78

DI_MCS_OK = 89
DI_QMC_MODE = 90
DI_FIXED_MOLD_HALF_MODE = 91
DI_FLAP_GOOD = 92
DI_FLAP_BAD = 93
DI_MOV_MOLD_HALF_MODE = 94

DI_PRESSURE_RELEASE_BTN = 112
DI_CORE_2_OUT = 113
DI_CORE_2_IN = 114



class IOMaker:
    def __init__(self, imm_type, board_1_modules_ios=None, board_2_modules_ios=None, big=False,
                 evaluation_num=None, production_num=None, type_string=None, customer=None,
                 safety_standard=None, technical_clause=None, dual_inj=False, external_hotrunner_num=0,
                 energy_dee=False, varan_conn_module_pos=0):
        '''
            imm_type:           'ZEs', 'ZE', 'VE2', 'VE2s'
            board_1_modules_ios: [['CTO163', {'DO3': OutputID, ...}], ['CDM163', {'DI5': InputID, ...}], ...]
            board_2_modules_ios:    [['CTO163', {'DO3': OutputID, ...}], ['CDM163', {'DI5': InputID, ...}], ...]
        '''
        # TODO: 数据库位置需要小心
        self.path_db = './app/libfiles/data.db'
        self.t_di = TableManager('digital_input', self.path_db)
        self.t_do = TableManager('digital_output', self.path_db)
        self.t_ai = TableManager('Analog_input', self.path_db)
        self.t_ao = TableManager('Analog_output', self.path_db)
        self.t_ti = TableManager('Temperature_input', self.path_db)
        self.t_to = TableManager('Temperature_output', self.path_db)

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
        self.external_hotrunner_num = external_hotrunner_num
        self.energy_dee = energy_dee
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
                              external_hotrunner_num=self.external_hotrunner_num,
                              energy_dee=self.energy_dee,
                              varan_conn_module_pos=varan_conn_module_pos)

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

    def createFile(self, path):
        self.xlsxObj.modifyImmInfo()

        self.xlsxObj.copyMainBoardModulesInfo()
        self.xlsxObj.copyMainBoardModules()
        self.xlsxObj.copyBoard1ModulesInfo()
        self.xlsxObj.copyBoard1Modules()
        self.xlsxObj.copyExternalHotrunnerInfo()
        self.xlsxObj.copyExternalHotrunnerModule()
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

