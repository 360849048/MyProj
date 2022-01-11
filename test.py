from app.configfile import *
import os
import re


def copySysfile(imm_type, cp, inj, inj_type, conv, ce):
  for root, dirs, files in os.walk(r"C:\Users\lenovo\Desktop\ls"):
    for file in files:
      os.remove(os.path.join(root, file))
    for dir in dirs:
      os.rmdir(os.path.join(root, dir))
  sysmaker = SysFileMaker(ce_standard=ce,
                          clamp_force=cp,
                          injection=inj,
                          inj_type=inj_type,
                          imm_type=imm_type,
                          conv=conv,
                          dst_file_dir=r"C:\Users\lenovo\Desktop\ls")
  ret = sysmaker.createFile()
  if ret < 0:
    print('*' * 20, imm_type, cp, inj, inj_type, conv, ce)

copySysfile('zes', 4500, 1400, 'h', False, True)

cp_list = []
# 获取所有合模组合 [(400, False), (3000, True), ...]
for file in os.listdir(r"F:\MyProj\app\libfiles\配置文件\系统文件\部件系统文件\合模系统文件"):
  cp = int(re.sub(r"[^0-9]", '', file))
  cp_list.append((cp, '变频器' in file))

inj_list = []
# 获取所有注射组合
for file in os.listdir(r"F:\MyProj\app\libfiles\配置文件\系统文件\部件系统文件\注射系统文件"):
  inj = int(re.sub(r"[^0-9]", '', file))
  inj_type = re.sub(r"INJ_[0-9]+", '', os.path.splitext(file)[0])
  inj_list.append((inj, inj_type))

# # 测试
# for cp_info in cp_list:
#   for inj_info in inj_list:
#     copySysfile('zes', cp_info[0], inj_info[0], inj_info[1], cp_info[1], True)
#     copySysfile('zes', cp_info[0], inj_info[0], inj_info[1], cp_info[1], False)
#     copySysfile('ve2s', cp_info[0], inj_info[0], inj_info[1], cp_info[1], True)
#     copySysfile('ve2s', cp_info[0], inj_info[0], inj_info[1], cp_info[1], False)
#     copySysfile('ze', cp_info[0], inj_info[0], inj_info[1], cp_info[1], True)
#     copySysfile('ze', cp_info[0], inj_info[0], inj_info[1], cp_info[1], False)
#     copySysfile('ve2', cp_info[0], inj_info[0], inj_info[1], cp_info[1], True)
#     copySysfile('ve2', cp_info[0], inj_info[0], inj_info[1], cp_info[1], False)