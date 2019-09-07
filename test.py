from app.user import verifyAccount, createAccount, modifyPwd, deleteAccount, modifyUsername

# print(verifyAccount('admin', '12345'))
# print(modifyPwd('admin', '123456'))
# print(modifyUsername('admin', 'J'))
# print(verifyAccount('admin', '123456'))
# createAccount(account="13555", password="13555", username="HAITIAN-J")

from app.pathinfo import *
from app.sqljob import TableManager

ret_data = {'status': True, 'releaseNote': {}}
t_std_ver = TableManager('t_vers', STD_SOFTWARE_RELEASE_NOTE_DB_PATH)
ids = t_std_ver.getAllId(orderby="version", desc=True)
print(ids)
ver_count = 0
for each_id in ids:
    print(each_id)
    ver_count += 1
    ver_info = t_std_ver.displayBriefData(each_id, "version", "origin", "release_note")
    ret_data['releaseNote'][ver_count] = {}
    ret_data['releaseNote'][ver_count]['version'] = ver_info[0]
    ret_data['releaseNote'][ver_count]['origin'] = ver_info[1]
    ret_data['releaseNote'][ver_count]['releaseNote'] = ver_info[2].split(';;;')
print(ret_data)
