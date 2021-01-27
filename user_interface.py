# -*- coding:utf-8 -*-
from tkinter import Tk
from tkinter import Frame
from tkinter import Button
from tkinter import Canvas
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
        self.window_width = int(self.main.window_width * self.scale_factor)
        self.window_height = int(self.main.window_height * self.scale_factor)
        self.window.geometry('{}x{}'.format(self.window_width, self.window_height)) #窗口大小
        self.window.resizable(0,0)      #锁定窗口大小

        self.init_frame_left()
        self.init_frame2()

        self.window.configure(cursor = 'heart')


    def dpi_adapt(self):
        '''解决高分屏下程序界面模糊问题（高DPI适配）'''
        if self.main.dpi_adapt:
            #设置由应用程序自己控制缩放
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            #获得显示设置的缩放因子
            self.scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
            #设置组件缩放
            self.window.tk.call('tk', 'scaling', self.scale_factor * 1.6)

    def init_frame_left(self):
        '''左边栏框架'''
        self.frame_left = Frame(
            self.window, 
            bd=self.window_width / 120, 
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
        self.init_indicator()

    def init_btn_add(self):
        '''左边栏新增开始/结束按钮'''
        self.btn_add = Button(
            self.frame_left, 
            text='新增开始/结束', 
            # font=('bold'),
            bd=self.window_width / 150, 
            relief='groove', 
            width=int(self.window_width / 53),
            height=3,
            bg='#DA70D6',   #orchid
            fg='#FFFFFF',   #white
            activebackground='#DA70D6',
            activeforeground='#FFFFFF'
        )
        self.btn_add.place(x=self.window_width * 0.029, y=self.window_height * 0.1, anchor='nw')

    def init_btn_callender(self):
        '''左边栏日历按钮'''
        self.btn_callender = Button(
            self.frame_left, 
            text='日历', 
            bd=self.window_width / 150, 
            relief='groove', 
            width=int(self.window_width / 75),
            height=1,
            bg='#FFF0F5',   #lavenderblush
            fg='#FF1493',   #deeppink
            activebackground='#FFF0F5',
            activeforeground='#FF1493'
        )
        self.btn_callender.place(x=self.window_width * 0.05, y=self.window_height * 19 / 60, anchor='nw')
    
    def init_btn_stats(self):
        '''左边栏统计数据按钮'''
        self.btn_stats = Button(
            self.frame_left, 
            text='统计数据', 
            bd=self.window_width / 150, 
            relief='groove', 
            width=int(self.window_width / 75),
            height=1,
            bg='#FFF0F5',   #lavenderblush
            fg='#FF1493',   #deeppink
            activebackground='#FFF0F5',
            activeforeground='#FF1493'
        )
        self.btn_stats.place(x=self.window_width * 0.05, y=self.window_height * 27 / 60, anchor='nw')

    def init_btn_list(self):
        '''左边栏查看记录按钮'''
        self.btn_list = Button(
            self.frame_left, 
            text='查看记录', 
            bd=self.window_width / 150, 
            relief='groove', 
            width=int(self.window_width / 75),
            height=1,
            bg='#FFF0F5',   #lavenderblush
            fg='#FF1493',   #deeppink
            activebackground='#FFF0F5',
            activeforeground='#FF1493'
        )
        self.btn_list.place(x=self.window_width * 0.05, y=self.window_height * 35 / 60, anchor='nw')

    def init_btn_settings(self):
        '''左边栏设置按钮'''
        self.btn_settings = Button(
            self.frame_left, 
            text='设置', 
            bd=self.window_width / 150, 
            relief='groove', 
            width=int(self.window_width / 75),
            height=1,
            bg='#FFF0F5',   #lavenderblush
            fg='#FF1493',   #deeppink
            activebackground='#FFF0F5',
            activeforeground='#FF1493'
        )
        self.btn_settings.place(x=self.window_width * 0.05, y=self.window_height * 43 / 60, anchor='nw')

    def init_btn_about(self):
        '''左边栏关于按钮'''
        self.btn_about = Button(
            self.frame_left, 
            text='关于', 
            bd=self.window_width / 150, 
            relief='groove', 
            width=int(self.window_width / 75),
            height=1,
            bg='#FFF0F5',   #lavenderblush
            fg='#FF1493',   #deeppink
            activebackground='#FFF0F5',
            activeforeground='#FF1493'
        )
        self.btn_about.place(x=self.window_width * 0.05, y=self.window_height * 51 / 60, anchor='nw')

    def init_indicator(self):
        '''左边栏指示标志（爱心）'''
        self.indicator = Canvas(
            self.frame_left, 
            highlightthickness=0,
            width=14 * self.window_width / 375,
            height=14 * self.window_width / 375,
            bg='#FFC0CB'    #pink
        )
        self.indicator.create_polygon(
            2 * self.window_width / 375, 0, 
            5 * self.window_width / 375, 0, 
            7 * self.window_width / 375, 2 * self.window_width / 375, 
            9 * self.window_width / 375, 0, 
            12 * self.window_width / 375, 0, 
            14 * self.window_width / 375, 3 * self.window_width / 375, 
            14 * self.window_width / 375, 6 * self.window_width / 375, 
            13 * self.window_width / 375, 8 * self.window_width / 375, 
            7 * self.window_width / 375, 14 * self.window_width / 375, 
            1 * self.window_width / 375, 8 * self.window_width / 375, 
            0, 6 * self.window_width / 375, 
            0, 3 * self.window_width / 375, 
            fill='#DA70D6',     #orchid
        )   #画一个多边形爱心
        self.indicator.place(x=self.window_width * 0.27, y=self.window_height * 27 / 60 + self.scale_factor * 8, anchor='ne')

    def init_frame2(self):
        self.frame2 = Frame(
            self.window, 
            bd=self.window_width / 120,
            relief='groove', 
            width=self.window_width * 0.7, 
            height=self.window_height,
            bg='#FFF0F5'    #lavenderblush
        )
        self.frame2.pack(side='right')
        self.frame2.pack_propagate(0)

if __name__ == '__main__':
    print('This is not the start file, please run "core.py".')
    input('Press "Enter" to quit.')