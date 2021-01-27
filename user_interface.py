# -*- coding:utf-8 -*-
from tkinter import Tk
from tkinter import Frame
from tkinter import Button
import ctypes

class UserInterface():
    '''用户界面，包括图形化窗口与交互逻辑'''

    def __init__(self, main):
        self.main = main
        self.window = Tk()
        self.window.iconbitmap('icon.ico')
        self.window.title('Period Calculator V%s' % self.main.version)
        
        self.scale_factor = 1   #默认缩放因子
        self.dpi_adapt()        #高DPI适配
        self.window_width = self.main.window_width * self.scale_factor
        self.window_height = self.main.window_height * self.scale_factor
        self.window.geometry('{}x{}'.format(self.window_width, self.window_height)) #窗口大小
        self.window.resizable(0,0)      #锁定窗口大小

        self.init_frame_left()
        self.init_frame2()


    def dpi_adapt(self):
        '''解决高分屏下程序界面模糊问题（高DPI适配）'''
        if self.main.dpi_adapt:
            #设置由应用程序自己控制缩放
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            #获得显示设置的缩放因子
            self.scale_factor = int(ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100)
            #设置组件缩放
            self.window.tk.call('tk', 'scaling', self.scale_factor * 1.6)

    def init_frame_left(self):
        self.frame_left = Frame(
            self.window, 
            bd=10, 
            relief='groove', 
            width=self.window_width * 0.3, 
            height=self.window_height,
            bg='#FFC0CB'    #pink
        )
        self.frame_left.pack(side='left')
        self.frame_left.pack_propagate(0)
        self.init_btn_add()
        self.init_btn_callender()
        self.init_btn_stats()
        self.init_btn_list()
        self.init_btn_settings()
        self.init_btn_about()

    def init_frame2(self):
        self.frame2 = Frame(
            self.window, 
            bd=10, 
            relief='groove', 
            width=self.window_width * 0.7, 
            height=self.window_height,
            bg='#FFF0F5'    #lavenderblush
        )
        self.frame2.pack(side='right')
        self.frame2.pack_propagate(0)

    def init_btn_add(self):
        self.btn_add = Button(
            self.frame_left, 
            text='新增开始/结束', 
            bd=6, 
            relief='groove', 
            width=14,
            height=3,
            bg='#DDA0DD',   #plum
            # fg='white'
        )
        self.btn_add.place(x=self.window_width * 0.03, y=self.window_height * 0.08, anchor='nw')

    def init_btn_callender(self):
        self.btn_callender = Button(
            self.frame_left, 
            text='日历', 
            bd=8, 
            relief='groove', 
            width=10,
            height=1,
            bg='#FFF0F5',   #lavenderblush
            fg='hotpink'
        )
        self.btn_callender.place(x=self.window_width * 0.05, y=self.window_height * 9 / 30, anchor='nw')
    
    def init_btn_stats(self):
        self.btn_stats = Button(
            self.frame_left, 
            text='统计数据', 
            bd=8, 
            relief='groove', 
            width=10,
            height=1,
            bg='#FFF0F5',   #lavenderblush
            fg='hotpink'
        )
        self.btn_stats.place(x=self.window_width * 0.05, y=self.window_height * 13 / 30, anchor='nw')

    def init_btn_list(self):
        self.btn_list = Button(
            self.frame_left, 
            text='查看记录', 
            bd=8, 
            relief='groove', 
            width=10,
            height=1,
            bg='#FFF0F5', 
            fg='hotpink'
        )
        self.btn_list.place(x=self.window_width * 0.05, y=self.window_height * 17 / 30, anchor='nw')

    def init_btn_settings(self):
        self.btn_settings = Button(
            self.frame_left, 
            text='设置', 
            bd=8, 
            relief='groove', 
            width=10,
            height=1,
            bg='#FFF0F5', 
            fg='hotpink'
        )
        self.btn_settings.place(x=self.window_width * 0.05, y=self.window_height * 21 / 30, anchor='nw')

    def init_btn_about(self):
        self.btn_about = Button(
            self.frame_left, 
            text='关于', 
            bd=8, 
            relief='groove', 
            width=10,
            height=1,
            bg='#FFF0F5', 
            fg='hotpink'
        )
        self.btn_about.place(x=self.window_width * 0.05, y=self.window_height * 25 / 30, anchor='nw')


if __name__ == '__main__':
    print('This is not the start file, please run "core.py".')
    input('Press "Enter" to quit.')