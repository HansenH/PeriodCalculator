from tkinter import Tk
from tkinter.ttk import Button  # win本地化主题模块，部件更美观
import ctypes

class UserInterface():
    '''用户界面，包括图形化窗口与交互逻辑'''

    def __init__(self, main):
        self.main = main
        self.window = Tk()
        self.window.iconbitmap('icon.ico')
        self.window.title('Period Calculator V%s' % self.main.version)
        self.window.geometry('{}x{}'.format(self.main.window_width, self.main.window_height))
        self.dpi_adapt()    #高DPI适配，删除此行可能导致字体和组件边缘模糊
        self.test()

    def dpi_adapt(self):
        '''解决高分屏下程序界面模糊问题（高DPI适配）'''
        #设置由应用程序自己控制缩放
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        #获得显示设置的缩放因子
        scale_factor = int(ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100)
        #设置缩放
        self.window.tk.call('tk', 'scaling', scale_factor * 1.5)
        self.window.geometry('{}x{}'.format(self.main.window_width * scale_factor, 
                                        self.main.window_height * scale_factor))

    def test(self):
        btn = Button(self.window, text="周期")
        btn.pack()





if __name__ == '__main__':
    print('This is not the start file, please run "core.py".')
    input('Press "Enter" to quit.')