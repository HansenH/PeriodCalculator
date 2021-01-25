# -*- coding:utf-8 -*-
from tkinter import Tk
from tkinter.ttk import Style
from tkinter.ttk import Button  # ttk: win本地化主题模块，组件更美观
from tkinter import Frame
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

        self.style = Style()
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
            bg='#FFC0CB', 
            bd=10, 
            relief='groove', 
            width=self.window_width * 0.3, 
            height=self.window_height
        )
        self.frame_left.pack(side='left')
        self.frame_left.pack_propagate(0)
        self.init_btn()

    def init_btn(self):
        sytle = Style().configure('TButton', background='red')
        self.btn = Button(self.frame_left, text='HHHH', style='TButton')
        
        self.btn.place(x=50, y=100, anchor='nw')


    def init_frame2(self):
        self.frame2 = Frame(
            self.window, 
            bg='#FFF0F5', 
            bd=10, 
            relief='groove', 
            width=self.window_width * 0.7, 
            height=self.window_height
        )
        self.frame2.pack(side='right')
        self.frame2.pack_propagate(0)




if __name__ == '__main__':
    print('This is not the start file, please run "core.py".')
    input('Press "Enter" to quit.')