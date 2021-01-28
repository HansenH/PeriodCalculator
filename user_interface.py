# -*- coding:utf-8 -*-
from tkinter import Tk
from tkinter import Frame
from tkinter import Button
from tkinter import Canvas
from tkinter import Label
import ctypes

class UserInterface():
    '''用户界面，包括图形化窗口与交互逻辑'''

    def __init__(self, main):
        self.main = main
        self.window = Tk()
        self.window.iconbitmap('icon.ico')
        self.window.title('Period Calculator V%s' % self.main.version)

        self.scale_factor = 1   #缩放因子
        self.dpi_adapt()        #高DPI适配
        self.window_width = int(self.main.window_width * self.scale_factor)     #窗口宽
        self.window_height = int(self.main.window_height * self.scale_factor)   #窗口高
        window_x = int((self.window.winfo_screenwidth() * self.scale_factor - self.window_width) / 2)   #窗口位置（居中）
        window_y = int((self.window.winfo_screenheight() * self.scale_factor - self.window_height) / 2) #窗口位置（居中）
        self.window.geometry('{}x{}+{}+{}'.format(self.window_width, self.window_height, window_x, window_y))
        self.window.resizable(False, False)      #锁定窗口大小

        self.init_frame_left()
        self.init_frame_stats()     #默认初始页
        self.last_frame = self.frame_stats  #前一次的页面
        self.click_stats()

        # self.window.configure(cursor = 'heart')


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
            width=14,
            height=3,
            bg='#DA70D6',   #orchid
            fg='#FFFFFF',   #white
            activebackground='#DA70D6',
            activeforeground='#FFFFFF'
        )
        self.btn_add.place(relx=0.5, y=self.window_height * 0.2, anchor='center')

    def init_btn_callender(self):
        '''左边栏日历按钮'''
        self.btn_callender = Button(
            self.frame_left, 
            text='日历', 
            bd=self.window_width / 150, 
            relief='groove', 
            width=10,
            height=1,
            bg='#FFF0F5',   #lavenderblush
            fg='#FF1493',   #deeppink
            activebackground='#FFF0F5',
            activeforeground='#FF1493'
        )
        self.btn_callender.place(relx=0.5, rely=0.35, anchor='center')
    
    def init_btn_stats(self):
        '''左边栏统计数据按钮'''
        self.btn_stats = Button(
            self.frame_left, 
            text='统计数据', 
            bd=self.window_width / 150, 
            relief='groove', 
            width=10,
            height=1,
            bg='#FFF0F5',   #lavenderblush
            fg='#FF1493',   #deeppink
            activebackground='#FFF0F5',
            activeforeground='#FF1493',
            command = self.click_stats
        )
        self.btn_stats.place(relx=0.5, rely=0.48, anchor='center')

    def init_btn_list(self):
        '''左边栏查看记录按钮'''
        self.btn_list = Button(
            self.frame_left, 
            text='查看记录', 
            bd=self.window_width / 150, 
            relief='groove', 
            width=10,
            height=1,
            bg='#FFF0F5',   #lavenderblush
            fg='#FF1493',   #deeppink
            activebackground='#FFF0F5',
            activeforeground='#FF1493'
        )
        self.btn_list.place(relx=0.5, rely=0.61, anchor='center')

    def init_btn_settings(self):
        '''左边栏设置按钮'''
        self.btn_settings = Button(
            self.frame_left, 
            text='设置', 
            bd=self.window_width / 150, 
            relief='groove', 
            width=10,
            height=1,
            bg='#FFF0F5',   #lavenderblush
            fg='#FF1493',   #deeppink
            activebackground='#FFF0F5',
            activeforeground='#FF1493'
        )
        self.btn_settings.place(relx=0.5, rely=0.74, anchor='center')

    def init_btn_about(self):
        '''左边栏关于按钮'''
        self.btn_about = Button(
            self.frame_left, 
            text='关于', 
            bd=self.window_width / 150, 
            relief='groove', 
            width=10,
            height=1,
            bg='#FFF0F5',   #lavenderblush
            fg='#FF1493',   #deeppink
            activebackground='#FFF0F5',
            activeforeground='#FF1493',
            command = self.click_about
        )
        self.btn_about.place(relx=0.5, rely=0.87, anchor='center')

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
        self.indicator.place(relx=0.9, rely=0.48, anchor='center')

    def init_frame_stats(self):
        '''统计数据页'''
        self.frame_stats = Frame(
            self.window, 
            bd=self.window_width / 120,
            relief='groove', 
            width=self.window_width * 0.7, 
            height=self.window_height,
            bg='#FFF0F5'    #lavenderblush
        )
        self.frame_stats.pack(side='right')
        self.frame_stats.pack_propagate(0)
        self.init_text_stats()

    def init_text_stats(self):
        '''统计数据文本'''
        self.main.show_stats()
        self.text_stats = Label(
            self.frame_stats,
            text=self.main.print_stats,
            justify='left',
            bg='#FFF0F5'    #lavenderblush
        )
        self.text_stats.place(relx=0.5, rely=0.1, anchor='n')

    def init_frame_about(self):
        '''关于页'''
        self.frame_about = Frame(
            self.window, 
            bd=self.window_width / 120,
            relief='groove', 
            width=self.window_width * 0.7, 
            height=self.window_height,
            bg='#FFF0F5'    #lavenderblush
        )
        self.frame_about.pack(side='right')
        self.frame_about.pack_propagate(0)
        self.init_text_about()

    def init_text_about(self):
        '''关于文本'''
        # self.main.show_about()
        self.text_about = Label(
            self.frame_about,
            text='about',
            justify='left',
            bg='#FFF0F5'    #lavenderblush
        )
        self.text_about.place(relx=0.5, rely=0.1, anchor='n')


    def click_stats(self):
        '''点击统计数据按钮'''
        self.indicator.place(relx=0.9, rely=0.48, anchor='center')  #移动爱心位置
        self.last_frame.destroy()       #关闭之前的右侧页面
        self.init_frame_stats()         #打开新的右侧页面
        self.last_frame = self.frame_stats

    def click_about(self):
        '''点击关于按钮'''
        self.indicator.place(relx=0.9, rely=0.87, anchor='center')
        self.last_frame.destroy()
        self.init_frame_about()
        self.last_frame = self.frame_about
        

if __name__ == '__main__':
    print('This is not the start file, please run "core.py".')