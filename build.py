import os
import shutil

web_path = './web/'
os.chdir(web_path)

os.system("npm run build")

for file_name in os.listdir('./dist/'):
    if file_name.endswith('.js'):
        src_path = os.path.join('./dist/', file_name)
        dst_path = os.path.join('../app/static/js/', file_name)
        shutil.copyfile(src_path, dst_path)

