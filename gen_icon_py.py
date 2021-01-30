# -*- coding:utf-8 -*-
'''
此脚本用来生成icon.py文件。
我们使用base64编码，把icon.ico图标作为变量保存在icon.py中，
使用pyinstaller打包exe后，可在执行中由该变量生成临时ico文件给tkinter调用，实现窗口图标。
从而exe文件可以独立运行，不再依赖目录中的ico文件。
'''
import base64

with open('icon.py', 'wb') as py_file_obj:
    text = "# -*- coding:utf-8 -*-\n'''\n"
    text += '此文件由gen_icon_py.py生成。\n我们使用base64编码，把icon.ico图标作为变量保存在icon.py中，\n'
    text += '使用pyinstaller打包exe后，可在执行中由该变量生成临时ico文件给tkinter调用，实现窗口图标。\n'
    text += '从而exe文件可以独立运行，不再依赖目录中的ico文件。\n'
    text += "'''\n\nencoded_img = '"
    py_file_obj.write(text.encode('utf-8'))
with open('icon.ico', 'rb') as ico_file_obj:
    b64str = base64.b64encode(ico_file_obj.read())
    with open('icon.py','ab') as py_file_obj:
        py_file_obj.write(b64str)
with open('icon.py','a') as py_file_obj:
    py_file_obj.write("'")