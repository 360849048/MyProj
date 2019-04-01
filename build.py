import os
import shutil


dst_path = os.path.join(os.getcwd(), './app/static/')
src_path = os.path.join(os.getcwd(), './web/dist/')

shutil.rmtree(dst_path)

web_path = './web/'
os.chdir(web_path)

os.system("npm run build")

shutil.copytree(src_path, dst_path)

