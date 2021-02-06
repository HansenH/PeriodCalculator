# -*- coding:utf-8 -*-
from tkinter import Tk
from tkinter import Frame
from tkinter import Button
from tkinter import Canvas
from tkinter import Label
from tkinter import Text
from tkinter import messagebox
from tkinter import Toplevel
from tkinter.ttk import Combobox
from datetime import date
import icon
import base64
import os
import ctypes
import webbrowser
import random

class UserInterface():
    '''用户界面，包括图形化窗口与交互逻辑'''

    def __init__(self, main):
        self.main = main
        self.window = Tk()
        self.window.withdraw()  #隐藏窗口(等到窗口宽高位置设定好后再显示)
        self.window.title('Period Calculator V%s' % self.main.version)  #窗口标题
        with open('temp.ico','wb') as temp_ico:     #生成临时ico图标文件
            temp_ico.write(base64.b64decode(icon.encoded_img))
        self.window.iconbitmap('temp.ico')      #设置窗口左上角图标
        os.remove('temp.ico')                   #删除临时ico图标文件

        self.scale_factor = 1   #缩放因子
        self.dpi_adapt()        #高DPI适配
        self.window_width = int(self.main.window_width * self.scale_factor)    
        self.window_height = int(self.main.window_height * self.scale_factor)   
        window_x = int((self.window.winfo_screenwidth() * self.scale_factor - self.window_width) / 2)
        window_y = int((self.window.winfo_screenheight() * self.scale_factor - self.window_height) / 2)
        self.window.geometry('{}x{}+{}+{}'.format(
            self.window_width,      #窗口宽
            self.window_height,     #窗口高
            window_x,          #窗口位置x
            window_y           #窗口位置y
        ))
        self.window.resizable(False, False)      #锁定窗口大小
        self.window.deiconify()     #显示窗口

        self.init_frame_left()      #初始化左边栏
        self.init_frame_stats()     #默认初始页=数据统计页
        self.current_frame = self.frame_stats  #记录当前页面引用
        #弹窗通知记录文件加载异常（如有）
        if self.main.load_error:
            messagebox.showwarning(message=self.main.error_msg)

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
        self.init_btn_calendar()
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
            activeforeground='#FFFFFF',
            command = self.click_add
        )
        self.btn_add.place(relx=0.5, rely=0.17, anchor='center')

    def init_btn_calendar(self):
        '''左边栏日历按钮'''
        self.btn_calendar = Button(
            self.frame_left, 
            text='日历', 
            bd=self.window_width / 150, 
            relief='groove', 
            width=10,
            height=1,
            bg='#FFF0F5',   #lavenderblush
            fg='#FF1493',   #deeppink
            activebackground='#FFF0F5',
            activeforeground='#FF1493',
            command = self.click_calendar
        )
        self.btn_calendar.place(relx=0.5, rely=0.35, anchor='center')
    
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
            13 * self.window_width / 375, 1 * self.window_width / 375, 
            14 * self.window_width / 375, 3 * self.window_width / 375, 
            14 * self.window_width / 375, 6 * self.window_width / 375, 
            13 * self.window_width / 375, 8 * self.window_width / 375, 
            7 * self.window_width / 375, 14 * self.window_width / 375, 
            1 * self.window_width / 375, 8 * self.window_width / 375, 
            0, 6 * self.window_width / 375, 
            0, 3 * self.window_width / 375, 
            1 * self.window_width / 375, 1 * self.window_width / 375,
            fill='#DA70D6',     #orchid
        )   #画一个多边形爱心
        self.indicator.place(relx=0.9, rely=0.48, anchor='center')

    def init_frame_calendar(self):
        '''日历页框架'''
        self.frame_calendar = Frame(
            self.window, 
            bd=self.window_width / 120,
            relief='groove', 
            width=self.window_width * 0.7, 
            height=self.window_height,
            bg='#FFF0F5'    #lavenderblush
        )
        self.frame_calendar.pack(side='right')
        self.frame_calendar.pack_propagate(0)
        self.init_calendar()

    def init_calendar(self):
        '''日历页'''
        text_calendar = Label(
            self.frame_calendar,
            text='此功能开发中...',
            justify='left',
            bg='#FFF0F5'    #lavenderblush
        )
        text_calendar.place(relx=0.5, rely=0.4, anchor='n')

    def init_frame_stats(self):
        '''统计数据页框架'''
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
        self.init_stats()

    def init_stats(self):
        '''统计数据页'''
        self.main.show_stats()

        #子框架，实现所有控件上下排列的同时整体居中
        frame_stats_amid = Frame(
            self.frame_stats, 
            bg='#FFF0F5'    #lavenderblush
        )
        frame_stats_amid.pack(side='top', expand='yes')

        text_ongoing = Label(
            frame_stats_amid,
            text=self.main.print_ongoing,
            bg='#FFF0F5'    #lavenderblush
        )
        text_ongoing.pack(side='top')

        def click_reset():
            ans = messagebox.askokcancel(message='您确定要取消进行中的经期吗？')
            if ans:
                self.main.reset()
                self.click_stats()

        if self.main.ongoing_date is not None:
            #重置按钮，点击后重置进行中的经期并刷新本页面
            btn_reset = Button(
                frame_stats_amid, 
                text='重置', 
                bd=3, 
                relief='groove', 
                bg='#FFF0F5',   #lavenderblush
                fg='#FF1493',   #deeppink
                activebackground='#FFF0F5',
                activeforeground='#FF1493',
                command = click_reset
            )
            btn_reset.pack(side='top', pady=self.window_height / 60)

        text_stats = Label(
            frame_stats_amid,
            text=self.main.print_stats,
            justify='left',
            bg='#FFF0F5'    #lavenderblush
        )
        text_stats.pack(side='top')

        text_future = Label(
            frame_stats_amid,
            text=self.main.print_future,
            justify='left',
            bg='#FFF0F5'    #lavenderblush
        )
        text_future.pack(side='top')

    def init_frame_about(self):
        '''关于页框架'''
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
        self.init_about()

    def init_about(self):
        '''关于页'''
        self.click_count = 0     #hidden触发计数器
        text_about = Text(
            self.frame_about,
            width=45,
            height=15,
            bd=0,
            relief='flat',
            cursor='arrow',
            bg='#FFF0F5'    #lavenderblush
        )
        text_about.insert('end','作者: HansenH\n\n')
        text_about.insert('end','邮箱: hansenh@foxmail.com\n\n')
        text_about.insert('end','源码(Python3): \n')
        text_about.insert('end','https://github.com/HansenH/PeriodCalculator\n\n')
        text_about.insert('end','\n\nMIT License\nCopyright (c) 2021 HansenH')

        text_about.tag_add('link','6.0','6.43')    #第六行超链接加tag
        text_about.tag_config('link', foreground='blue', underline = True)
        text_about.tag_add('hidden','1.4','1.11')  #第一行HansenH加tag

        def show_hand_cursor(event):
            text_about.configure(cursor='hand2')
        def show_arrow_cursor(event):
            text_about.configure(cursor='arrow')
        def click_link(event):
            webbrowser.open_new_tab('https://github.com/HansenH/PeriodCalculator')

        def show_heart_cursor(event):
            text_about.configure(cursor='heart')
            self.click_count = 0    #鼠标进入或离开'HansenH'都会重置计数器self.self.click_count
        def show_arrow_cursor2(event):
            text_about.configure(cursor='arrow')
            self.click_count = 0
        def click_hidden_5_times(event):
            self.click_count += 1
            if self.click_count == 5:
                self.hidden()    #触发hidden Easter Egg!

        text_about.tag_bind('link', '<Enter>', show_hand_cursor)   #鼠标指向
        text_about.tag_bind('link', '<Leave>', show_arrow_cursor)  #鼠标离开
        text_about.tag_bind('link', '<Button-1>', click_link)      #左键点击
        text_about.tag_bind('hidden', '<Enter>', show_heart_cursor)  #鼠标指向
        text_about.tag_bind('hidden', '<Leave>', show_arrow_cursor2) #鼠标离开
        text_about.tag_bind('hidden', '<Button-1>', click_hidden_5_times)#触发hidden
        text_about.place(relx=0.5, rely=0.2, anchor='n')

    def click_add(self):
        '''点击新增按钮，创建模态对话框'''
        dialog_add = Toplevel()     #弹出对话框
        dialog_add.wm_transient(self.window)    #与父窗口关联，窗口管理器不会当成独立窗口
        dialog_add.focus_set()      #焦点切换到对话框
        dialog_add.grab_set()       #事件不会传入父窗口(父窗口无法点击)
        dialog_add.withdraw()       #隐藏窗口(等到窗口宽高位置设定好后再显示)
        dialog_add.title('添加经期开始/结束')     #窗口标题




        frame_add = Frame(
            dialog_add, 
            padx = self.window_width / 40,
            pady = self.window_width / 40,
            bg='#FFF0F5'    #lavenderblush
        )
        frame_add.pack()

        # frame_add_amid = Frame(
        #     frame_add, 
        #     # padx = self.window_width / 60,
        #     # pady = self.window_width / 60,
        #     bg='#FFF0F5'    #lavenderblush
        # )
        # frame_add_amid.pack()

        #下拉选项默认值=今天日期
        default_yyyy = date.today().year
        default_mm = date.today().month
        default_dd = date.today().day




        box_yyyy = Combobox(frame_add, width=4, state='readonly')
        box_yyyy['value'] = tuple(range(1990, default_yyyy + 1))
        box_yyyy.current(default_yyyy - 1990)
        box_yyyy.pack(side='left', anchor='nw')

        label_year = Label(frame_add, text='年  ', bg='#FFF0F5')
        label_year.pack(side='left', anchor='nw')

        box_mm = Combobox(frame_add, width=2, state='readonly')
        box_mm['value'] = tuple(range(1, 13))
        box_mm.current(default_mm - 1)
        box_mm.pack(side='left', anchor='nw')

        label_month = Label(frame_add, text='月  ', bg='#FFF0F5')
        label_month.pack(side='left', anchor='nw')

        box_dd = Combobox(frame_add, width=2, state='readonly')
        box_dd['value'] = tuple(range(1, 32))
        box_dd.current(default_dd - 1)
        box_dd.pack(side='left', anchor='nw')

        label_day = Label(frame_add, text='日', bg='#FFF0F5')
        label_day.pack(side='left', anchor='nw')

        dialog_add.update_idletasks()   #手动更新显示，以便获得布局后的窗口宽高
        add_window_x = int((dialog_add.winfo_screenwidth() * self.scale_factor - dialog_add.winfo_width()) / 2)
        add_window_y = int((dialog_add.winfo_screenheight() * self.scale_factor - dialog_add.winfo_height()) / 2)
        dialog_add.geometry('+{}+{}'.format(add_window_x, add_window_y)) #设置窗口位置
        dialog_add.resizable(False, False)      #锁定窗口大小
        dialog_add.deiconify()      #显示窗口
        dialog_add.wait_window()    #进入















    def click_calendar(self):
        '''点击日历按钮'''
        self.indicator.place(relx=0.9, rely=0.35, anchor='center')  #移动爱心位置
        self.current_frame.destroy()       #关闭当前的右侧页面
        self.init_frame_calendar()      #打开新的右侧页面
        self.current_frame = self.frame_calendar

    def click_stats(self):
        '''点击统计数据按钮'''
        self.indicator.place(relx=0.9, rely=0.48, anchor='center')  #移动爱心位置
        self.current_frame.destroy()       #关闭当前的右侧页面
        self.init_frame_stats()         #打开新的右侧页面
        self.current_frame = self.frame_stats

    def click_about(self):
        '''点击关于按钮'''
        self.indicator.place(relx=0.9, rely=0.87, anchor='center')  #移动爱心位置
        self.current_frame.destroy()       #关闭当前的右侧页面
        self.init_frame_about()         #打开新的右侧页面
        self.current_frame = self.frame_about
        
    def hidden(self):
        '''Easter Egg!'''
        self.current_frame.destroy()           #销毁原右侧页面
        self.frame_left.pack_forget()       #暂时隐藏左边栏
        heart_rain = Canvas(
            self.window, 
            highlightthickness=0,
            width=self.window_width,
            height=self.window_height,
            cursor='heart',
            bg='#FFF0F5'    #lavenderblush
        )
        heart_rain.place(relx=0.5, rely=0.5, anchor='center')

        heart_rain.create_text(
            0.5 *self.window_width,
            0.35 * self.window_height,
            text='This app is made for my beloved girl Wang Ting.',
            font=('Times', 12, 'bold italic'),
            anchor='center'
        )
        heart_rain.create_text(
            0.5 *self.window_width,
            0.85 * self.window_height,
            text='<返回>',
            anchor='center',
            tag='back'
        )

        def create_heart(size_factor, relx, rely):
            '''生成爱心(尺寸倍率, 相对x坐标, 相对y坐标),锚点=S'''
            heart = heart_rain.create_polygon(
                -5 * size_factor * self.window_width / 375 + relx * self.window_width, -14 * size_factor * self.window_width / 375 + rely * self.window_height, 
                -2 * size_factor * self.window_width / 375 + relx * self.window_width, -14 * size_factor * self.window_width / 375 + rely * self.window_height, 
                0 * size_factor * self.window_width / 375 + relx * self.window_width, -12 * size_factor * self.window_width / 375 + rely * self.window_height, 
                2 * size_factor * self.window_width / 375 + relx * self.window_width, -14 * size_factor * self.window_width / 375 + rely * self.window_height, 
                5 * size_factor * self.window_width / 375 + relx * self.window_width, -14 * size_factor * self.window_width / 375 + rely * self.window_height, 
                6 * size_factor * self.window_width / 375 + relx * self.window_width, -13 * size_factor * self.window_width / 375 + rely * self.window_height, 
                7 * size_factor * self.window_width / 375 + relx * self.window_width, -11 * size_factor * self.window_width / 375 + rely * self.window_height, 
                7 * size_factor * self.window_width / 375 + relx * self.window_width, -8 * size_factor * self.window_width / 375 + rely * self.window_height, 
                6 * size_factor * self.window_width / 375 + relx * self.window_width, -6 * size_factor * self.window_width / 375 + rely * self.window_height, 
                0 * size_factor * self.window_width / 375 + relx * self.window_width, 0 * size_factor * self.window_width / 375 + rely * self.window_height, 
                -6 * size_factor * self.window_width / 375 + relx * self.window_width, -6 * size_factor * self.window_width / 375 + rely * self.window_height, 
                -7 * size_factor * self.window_width / 375 + relx * self.window_width, -8 * size_factor * self.window_width / 375 + rely * self.window_height, 
                -7 * size_factor * self.window_width / 375 + relx * self.window_width, -11 * size_factor * self.window_width / 375 + rely * self.window_height, 
                -6 * size_factor * self.window_width / 375 + relx * self.window_width, -13 * size_factor * self.window_width / 375 + rely * self.window_height,
                fill='#FF1493',     #deeppink
            )
            return heart
        
        # 尺寸--速度--出现概率
        # 0.5--1--0.533  1--2--0.267  2--4--0.133  4--8--0.067
        # 生成位置：relx范围 -0.1~1.1  rely=-0.1
        hearts = []      #爱心队列
        speed = []      #每个爱心的速度
        PRODUCTION_RATE = 10    #每一帧生成新爱心的概率(%)

        def heart_drop_loop():
            '''实现爱心不断下落的循环'''
            #生成爱心
            if random.randint(0, 99) < PRODUCTION_RATE:
                rand_num = random.randint(0, 999)   #四种爱心按不同概率生成
                if rand_num < 533:
                    hearts.append(create_heart(0.5, random.randint(-100, 1100) / 1000, 0))
                    speed.append(1)
                elif 533 <= rand_num < 800:
                    hearts.append(create_heart(1, random.randint(-100, 1100) / 1000, 0))
                    speed.append(2)
                elif 800 <= rand_num < 933:
                    hearts.append(create_heart(2, random.randint(-100, 1100) / 1000, 0))
                    speed.append(4)
                else:
                    hearts.append(create_heart(4, random.randint(-100, 1100) / 1000, 0))
                    speed.append(8)
            #下移爱心
            for i in range(len(hearts) - 1, -1, -1):
                heart_rain.move(hearts[i], 0, speed[i] * 0.75)
                #删除出界的爱心（注意应当在倒序循环中删除元素）
                if heart_rain.coords(hearts[i])[1] > self.window_height:
                    heart_rain.delete(hearts.pop(i))
                    del speed[i]

            heart_rain.after(10, heart_drop_loop)  #after实现一段时间后再次调用自己
            #如果改用while和time.sleep()实现，会形成阻塞，无法在循环中监测事件！
        
        def back(event):
            '''返回'''
            heart_rain.destroy()
            self.frame_left.pack(side='left')
            self.frame_left.pack_propagate(0)
            self.init_frame_about()
            self.current_frame = self.frame_about

        heart_rain.tag_bind('back', '<Button-1>', back)
        heart_drop_loop()

    def refresh(self):
        '''(在记录改动后)刷新当前页面'''
        if self.current_frame == self.frame_stats:
            self.click_stats()
        # elif self.current_frame == self.frame_list:
        #     self.click_list()


if __name__ == '__main__':
    print('This is not the start file, please run "main.py".')