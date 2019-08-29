from app.user import verifyAccount, createAccount, modifyPwd, deleteAccount, modifyUsername

print(verifyAccount('admin', '12345'))
print(modifyPwd('admin', '123456'))
print(modifyUsername('admin', 'J'))
print(verifyAccount('admin', '123456'))