from src.sqljob import TableManager
from src.exceler import IOFile


class IOMaker:
    def __init__(self, imm_type, main_board_modules=None, board_1_modules=None, big=False):
        ''' imm_type:           'ZEs', 'ZE', 'VE2', 'VE2s'
                    main_board_modules: [['CTO163', {'O3': OutputID, ...}], ['CDM163', {'I5': InputID, ...}], ...]
                    board_1_modules:    [['CTO163', {'O3': OutputID, ...}], ['CDM163', {'I5': InputID, ...}], ...]
        '''
        self.path_db = '../libfiles/data.db'
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
        if main_board_modules is not None:
            self.main_board_modules = main_board_modules.copy()
            for module in self.main_board_modules:
                for io in module[1]:
                    id = module[1][io]
                    if str(io).upper().startswith('I'):
                        module[1][io] = self.t_di.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('O'):
                        module[1][io] = self.t_do.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('AI'):
                        module[1][io] = self.t_ai.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('AO'):
                        module[1][io] = self.t_ao.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('TI'):
                        module[1][io] = self.t_ti.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('TO'):
                        module[1][io] = self.t_to.displayBriefData(id, 'CName', 'EName')

        if board_1_modules is not None:
            self.board_1_modules = board_1_modules.copy()
            for module in self.board_1_modules:
                for io in module[1]:
                    id = module[1][io]
                    if str(io).upper().startswith('I'):
                        module[1][io] = self.t_di.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('O'):
                        module[1][io] = self.t_do.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('AI'):
                        module[1][io] = self.t_ai.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('AO'):
                        module[1][io] = self.t_ao.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('TI'):
                        module[1][io] = self.t_ti.displayBriefData(id, 'CName', 'EName')
                    if str(io).upper().startswith('TO'):
                        module[1][io] = self.t_to.displayBriefData(id, 'CName', 'EName')


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
    iomaker = IOMaker(imm_type='zes',
                      main_board_modules=[
                          ['cdm163', {'I1': 73, 'i2': 74, 'o1': 73, 'O2': 74}],
                          ['cto163', {'O1': 41, 'o2': 43, 'o3': 45}],
                          ['cam124', {'AI1': 2}]
                      ],
                      board_1_modules=[
                          ['civ512', {}],
                          ['cai888', {}],
                          ['cam124', {'AO1': 4}]
                      ],
                      big=False)
    iomaker.createIOFile()

