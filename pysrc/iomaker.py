from pysrc.sqljob import TableManager
from pysrc.exceler import IOFile


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
    def __init__(self, imm_type, board_1_modules=None, board_2_modules=None, big=False):
        ''' imm_type:           'ZEs', 'ZE', 'VE2', 'VE2s'
                    board_1_modules: [['CTO163', {'O3': OutputID, ...}], ['CDM163', {'I5': InputID, ...}], ...]
                    board_2_modules:    [['CTO163', {'O3': OutputID, ...}], ['CDM163', {'I5': InputID, ...}], ...]
        '''
        self.path_db = './libfiles/data.db'
        self.t_di = TableManager('digital_input', self.path_db)
        self.t_do = TableManager('digital_output', self.path_db)
        self.t_ai = TableManager('Analog_input', self.path_db)
        self.t_ao = TableManager('Analog_output', self.path_db)
        self.t_ti = TableManager('Temperature_input', self.path_db)
        self.t_to = TableManager('Temperature_output', self.path_db)
        self.imm_type = imm_type
        self.main_board_modules = None
        self.board_1_modules = None
        self.big = big
        if board_1_modules is not None:
            self.main_board_modules = board_1_modules.copy()
            for module in self.main_board_modules:
                for io in module[1]:
                    id = int(module[1][io])
                    if str(io).upper().startswith('DI'):
                        module[1][io] = self.t_di.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('DO'):
                        module[1][io] = self.t_do.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('AI'):
                        module[1][io] = self.t_ai.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('AO'):
                        module[1][io] = self.t_ao.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('TI'):
                        module[1][io] = self.t_ti.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('TO'):
                        module[1][io] = self.t_to.displayBriefData(id, 'CName', 'EName')

        if board_2_modules is not None:
            self.board_1_modules = board_2_modules.copy()
            for module in self.board_1_modules:
                for io in module[1]:
                    id = int(module[1][io])
                    if str(io).upper().startswith('DI'):
                        module[1][io] = self.t_di.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('DO'):
                        module[1][io] = self.t_do.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('AI'):
                        module[1][io] = self.t_ai.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('AO'):
                        module[1][io] = self.t_ao.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('TI'):
                        module[1][io] = self.t_ti.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('TO'):
                        module[1][io] = self.t_to.displayBriefData(id, 'CName', 'EName')
        print(self.main_board_modules)

    def createIOFile(self):
        file = IOFile(imm_type=self.imm_type,
                      main_board_modules=self.main_board_modules,
                      board_1_modules=self.board_1_modules,
                      big=self.big)
        file.copyMainBoardModulesInfo()
        file.copyMainBoardModules()
        file.copyBoard1ModulesInfo()
        file.copyBoard1Modules()
        file.saveAs('../1.xlsx')


if __name__ == '__main__':
    # 功能测试
    iomaker = IOMaker(imm_type='ZEs',
                      board_1_modules=[
                          ['cdm163', {
                              'I1': DI_PROGRAMMABLE_1,
                              'I2': DI_PROGRAMMABLE_2,
                              'I3': DI_PROGRAMMABLE_3,
                              'I4': DI_PROGRAMMABLE_4,
                              'I5': DI_PROGRAMMABLE_5,
                              'I6': DI_PROGRAMMABLE_6,
                              'O1': DO_PROGRAMMABLE_1,
                              'O2': DO_PROGRAMMABLE_2,
                              'O3': DO_PROGRAMMABLE_3,
                              'O4': DO_PROGRAMMABLE_4,
                              'O5': DO_PROGRAMMABLE_5,
                              'O6': DO_PROGRAMMABLE_6
                          }],
                          ['CDM163', {
                              'i1': DI_PRESSURE_RELEASE_BTN,
                              'i2': DI_CORE_2_IN,
                              'i3': DI_CORE_2_OUT,
                              'o1': DO_PRESSURE_RELEASE,
                              'O2': DO_CORE_2_IN_END,
                              'O3': DO_CORE_2_OUT_END,
                              'O4': DO_BAD_PRODUCT_2
                          }]
                      ],
                      board_2_modules=[
                          ['civ512', {}],
                          ['cai888', {}],
                      ],
                      big=False)
    iomaker.createIOFile()

