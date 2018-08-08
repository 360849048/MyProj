import os
import shutil

web_path = './web/'
os.chdir(web_path)

os.system("npm run build")
src_path = './dist/build.js'
dst_path = '../app/static/js/build.js'
shutil.copyfile(src_path, dst_path)
