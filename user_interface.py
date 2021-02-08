# -*- coding:utf-8 -*-
from tkinter import Tk
from tkinter import Frame
from tkinter import Button
from tkinter import Canvas
from tkinter import Label
from tkinter import Text
from tkinter import messagebox
from tkinter import Toplevel
from tkinter import Checkbutton
from tkinter import BooleanVar
from tkinter import Listbox
from tkinter import Scrollbar
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
            try:
                #设置由应用程序自己控制缩放
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
                #获得显示设置的缩放因子
                self.scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
                #设置缩放
                self.window.tk.call('tk', 'scaling', self.scale_factor * 1.6)
            except Exception:
                pass

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
            bd=self.window_width / 150, 
            relief='groove', 
            width=14,
            height=3,
            bg='#DA70D6',   #orchid
            fg='#FFFFFF',   #white
            activebackground='#DA70D6',
            activeforeground='#FFFFFF',
            command=self.click_add
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
            command=self.click_calendar
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
            command=self.click_stats
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
            activeforeground='#FF1493',
            command=self.click_list
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
            activeforeground='#FF1493',
            command=self.click_settings
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
            command=self.click_about
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
            ans = messagebox.askokcancel(message='确定要取消进行中的经期吗？')
            if ans:
                self.main.reset()
                self.click_stats()

        if self.main.ongoing_date is not None:
            #重置按钮，点击后重置进行中的经期并刷新本页面
            btn_reset = Button(
                frame_stats_amid, 
                text='重置', 
                bd=2, 
                relief='groove', 
                bg='#FFFFFF',   #white
                fg='#FF1493',   #deeppink
                activebackground='#FFFFFF',
                activeforeground='#FF1493',
                command=click_reset
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

    def init_frame_list(self):
        '''查看记录页框架'''
        self.frame_list = Frame(
            self.window, 
            bd=self.window_width / 120,
            relief='groove', 
            width=self.window_width * 0.7, 
            height=self.window_height,
            bg='#FFF0F5'    #lavenderblush
        )
        self.frame_list.pack(side='right')
        self.frame_list.pack_propagate(0)
        self.init_list()

    def init_list(self):
        '''查看记录页'''
        self.main.show_list()

        label_list_titles = Label(
            self.frame_list, 
            text='\n序号        起始日期       持续天数    间隔天数',
            bg='#FFF0F5'    #lavenderblush
        )
        label_list_titles.pack(side='top', anchor='w', padx=self.window_width / 40)

        frame_list_top = Frame(
            self.frame_list, 
            padx=self.window_width / 40,
            bg='#FFF0F5'    #lavenderblush
        )
        frame_list_top.pack(side='top', fill='x')

        #滚动条控件
        scrollbar_list = Scrollbar(frame_list_top, orient='vertical')
        scrollbar_list.pack(side='right', anchor='n', fill='y')

        listbox_list = Listbox(
            frame_list_top,
            activestyle='none',
            selectmode='single',
            height=20,
            font=('consolas', 10),
            yscrollcommand=scrollbar_list.set   #列表绑定滚动条
        )
        listbox_list.insert('end', *self.main.print_list)       #载入全部记录
        listbox_list.insert('end', '  +')              #末尾空行方便插入最新记录
        listbox_list.pack(side='right', anchor='n', expand='yes', fill='x')

        scrollbar_list.configure(command=listbox_list.yview)    #滚动条绑定列表
        listbox_list.yview_moveto(1)        #视图默认滚动到底
        # listbox_list.selection_set(self.main.count - 1)
        # listbox_list.event_generate("<<ListboxSelect>>")    #默认选择最后一条记录

        frame_list_bottom = Frame(
            self.frame_list, 
            padx=self.window_width / 40,
            pady=self.window_height / 20,
            bg='#FFF0F5'    #lavenderblush
        )
        frame_list_bottom.pack(side='top', fill='x')

        def click_insert():
            '''点击插入记录'''
            if len(listbox_list.curselection()) == 1:
                index = listbox_list.curselection()[0]

                dialog_insert = Toplevel()     #弹出对话框
                dialog_insert.wm_transient(self.window)    #与父窗口关联，窗口管理器不会当成独立窗口
                dialog_insert.focus_set()      #焦点切换到对话框
                dialog_insert.grab_set()       #事件不会传入父窗口(父窗口无法点击)
                dialog_insert.withdraw()       #隐藏窗口(等到窗口宽高位置设定好后再显示)
                dialog_insert.title('插入经期记录 (第{}行)'.format(index + 1)) #窗口标题

                frame_insert = Frame(
                    dialog_insert, 
                    padx = self.window_width / 20,
                    pady = self.window_width / 20,
                    bg='#FFF0F5'    #lavenderblush
                )
                frame_insert.pack()

                #以下为开始日期控件组

                frame_insert_fromdate = Frame(
                    frame_insert, 
                    bg='#FFF0F5'    #lavenderblush
                )
                frame_insert_fromdate.pack(side='top', anchor='s')

                label_from = Label(frame_insert_fromdate, text='开始日期：  ', bg='#FFF0F5')
                label_from.pack(side='left', anchor='n')

                box_yyyy1 = Combobox(frame_insert_fromdate, width=4, state='readonly')   #年选项框
                box_yyyy1['value'] = tuple(range(2000, date.today().year + 1))
                box_yyyy1.current(date.today().year - 2000)      #默认值为今天
                box_yyyy1.pack(side='left', anchor='n')

                label_year1 = Label(frame_insert_fromdate, text='年  ', bg='#FFF0F5')
                label_year1.pack(side='left', anchor='n')

                box_mm1 = Combobox(frame_insert_fromdate, width=2, state='readonly')     #月选项框
                box_mm1['value'] = tuple(range(1, 13))
                box_mm1.current(date.today().month - 1)          #默认值为今天
                box_mm1.pack(side='left', anchor='n')

                label_month1 = Label(frame_insert_fromdate, text='月  ', bg='#FFF0F5')
                label_month1.pack(side='left', anchor='n')

                box_dd1 = Combobox(frame_insert_fromdate, width=2, state='readonly')     #日选项框
                box_dd1['value'] = tuple(range(1, 32))
                box_dd1.current(date.today().day - 1)            #默认值为今天
                box_dd1.pack(side='left', anchor='n')

                label_day1 = Label(frame_insert_fromdate, text='日\n', bg='#FFF0F5')
                label_day1.pack(side='left', anchor='n')

                #以下为结束日期控件组

                frame_insert_todate = Frame(
                    frame_insert, 
                    bg='#FFF0F5'    #lavenderblush
                )
                frame_insert_todate.pack(side='top', anchor='s')

                label_to = Label(frame_insert_todate, text='结束日期：  ', bg='#FFF0F5')
                label_to.pack(side='left', anchor='n')

                box_yyyy2 = Combobox(frame_insert_todate, width=4, state='readonly')   #年选项框
                box_yyyy2['value'] = tuple(range(2000, date.today().year + 1))
                box_yyyy2.current(date.today().year - 2000)      #默认值为今天
                box_yyyy2.pack(side='left', anchor='n')

                label_year2 = Label(frame_insert_todate, text='年  ', bg='#FFF0F5')
                label_year2.pack(side='left', anchor='n')

                box_mm2 = Combobox(frame_insert_todate, width=2, state='readonly')     #月选项框
                box_mm2['value'] = tuple(range(1, 13))
                box_mm2.current(date.today().month - 1)          #默认值为今天
                box_mm2.pack(side='left', anchor='n')

                label_month2 = Label(frame_insert_todate, text='月  ', bg='#FFF0F5')
                label_month2.pack(side='left', anchor='n')

                box_dd2 = Combobox(frame_insert_todate, width=2, state='readonly')     #日选项框
                box_dd2['value'] = tuple(range(1, 32))
                box_dd2.current(date.today().day - 1)            #默认值为今天
                box_dd2.pack(side='left', anchor='n')

                label_day2 = Label(frame_insert_todate, text='日\n\n', bg='#FFF0F5')
                label_day2.pack(side='left', anchor='n')

                def insert():
                    '''点击对话框中的插入记录按钮'''
                    #获取开始日期
                    yyyy1 = int(box_yyyy1.get())
                    mm1 = int(box_mm1.get())
                    dd1 = int(box_dd1.get())

                    #获取结束日期
                    yyyy2 = int(box_yyyy2.get())
                    mm2 = int(box_mm2.get())
                    dd2 = int(box_dd2.get())

                    self.main.insert(index, yyyy1, mm1, dd1, yyyy2, mm2, dd2)
                    if self.main.add_error:     
                        #插入记录异常
                        messagebox.showinfo(message=self.main.error_msg, parent=dialog_insert)
                    else:
                        #插入记录成功
                        dialog_insert.destroy()    #关闭对话框
                        self.refresh()          #刷新页面相关信息
                        messagebox.showinfo(message='插入记录成功！')

                #对话框的插入记录按钮
                btn_insert_enter = Button(
                    frame_insert, 
                    text='插入记录',
                    bd=2, 
                    relief='groove', 
                    bg='#FFFFFF',   #white
                    fg='#FF1493',   #deeppink
                    activebackground='#FFFFFF',
                    activeforeground='#FF1493',
                    command=insert
                )
                btn_insert_enter.pack(side='top', anchor='n')

                dialog_insert.update_idletasks()   #手动更新显示，以获得布局后的窗口宽高来设置窗口位置
                dialog_insert_x = int((dialog_insert.winfo_screenwidth() * self.scale_factor - dialog_insert.winfo_width()) / 2)
                dialog_insert_y = int((dialog_insert.winfo_screenheight() * self.scale_factor - dialog_insert.winfo_height()) / 2)
                dialog_insert.geometry('+{}+{}'.format(dialog_insert_x, dialog_insert_y)) #设置窗口位置
                dialog_insert.resizable(False, False)      #锁定窗口大小
                dialog_insert.deiconify()      #显示窗口
                # dialog_insert.wait_window()

        #插入记录按钮
        btn_insert = Button(
            frame_list_bottom, 
            text='在选中行上方\n插入记录', 
            height=2,
            bd=2, 
            relief='groove', 
            bg='#FFFFFF',   #white
            fg='#FF1493',   #deeppink
            activebackground='#FFFFFF',
            activeforeground='#FF1493',
            command=click_insert
        )
        btn_insert.pack(side='left', expand='yes')

        def delete():
            '''点击删除选中记录'''
            if len(listbox_list.curselection()) == 1:
                index = listbox_list.curselection()[0]
                if index < self.main.count:
                    ans = messagebox.askokcancel(message='确定要删除选中的记录吗？')
                    if ans:
                        self.main.delete(index)
                        self.click_list()

        #删除选中记录按钮
        btn_delete = Button(
            frame_list_bottom, 
            text='删除选中记录', 
            height=2,
            bd=2, 
            relief='groove', 
            bg='#FFFFFF',   #white
            fg='#FF1493',   #deeppink
            activebackground='#FFFFFF',
            activeforeground='#FF1493',
            command=delete
        )
        btn_delete.pack(side='left', expand='yes')

        def delete_all():
            '''点击删除全部记录'''
            if self.main.count > 0:
                ans = messagebox.showwarning(title='警告', message='危险操作')
                if ans:
                    ans = messagebox.askokcancel(title='警告：危险操作', message='确定要删除全部记录吗?')
                    if ans:
                        ans = messagebox.askokcancel(title='点击确定将删除全部记录', message='真的要删除全部记录吗?')
                        if ans:
                            self.main.delete_all()
                            self.click_list()

        #删除全部记录按钮
        btn_delete_all = Button(
            frame_list_bottom, 
            text='删除全部记录', 
            height=2,
            bd=2, 
            relief='groove', 
            bg='#FFFFFF',   #white
            fg='#FF1493',   #deeppink
            activebackground='#FFFFFF',
            activeforeground='#FF1493',
            command=delete_all
        )
        btn_delete_all.pack(side='left', expand='yes')

    def init_frame_settings(self):
        '''设置页框架'''
        self.frame_settings = Frame(
            self.window, 
            bd=self.window_width / 120,
            relief='groove', 
            width=self.window_width * 0.7, 
            height=self.window_height,
            bg='#FFF0F5'    #lavenderblush
        )
        self.frame_settings.pack(side='right')
        self.frame_settings.pack_propagate(0)
        self.init_settings()

    def init_settings(self):
        '''设置页'''

        def change_dpi_adapt():
            '''更改dpi_adapt设置项'''
            self.main.dpi_adapt = self.dpi_adapt.get()
            self.main.save_settings()

        #设置项：高dpi屏幕显示缩放适配
        self.dpi_adapt = BooleanVar(value=self.main.dpi_adapt)  #选框默认值。必须设为实例变量，否则会被回收
        checkbox_dpi_adapt = Checkbutton(
            self.frame_settings, 
            text='高dpi屏幕显示缩放适配（重启应用后生效）', 
            variable=self.dpi_adapt,
            onvalue=True, 
            offvalue=False,
            bg='#FFF0F5',    #lavenderblush
            activebackground='#FFF0F5',
            command=change_dpi_adapt
            )
        checkbox_dpi_adapt.pack(side='top', padx=self.window_width / 20,
                pady=self.window_height / 20, anchor='nw')

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
            padx = self.window_width / 20,
            pady = self.window_width / 20,
            bg='#FFF0F5'    #lavenderblush
        )
        frame_add.pack()

        def add():
            '''点击对话框中的添加记录按钮'''
            yyyy = int(box_yyyy.get())      #从下拉选项框获取数据
            mm = int(box_mm.get())
            dd = int(box_dd.get())
            self.main.add(yyyy, mm, dd)     #添加经期开始/结束
            if self.main.add_error:     
                #添加记录异常
                messagebox.showinfo(message=self.main.error_msg, parent=dialog_add)
            else:
                #添加记录成功
                dialog_add.destroy()    #关闭对话框
                self.refresh()          #刷新页面相关信息
                messagebox.showinfo(message='添加记录成功！')

        #添加记录的按钮
        btn_add_enter = Button(
            frame_add, 
            bd=2, 
            relief='groove', 
            bg='#FFFFFF',   #white
            fg='#FF1493',   #deeppink
            activebackground='#FFFFFF',
            activeforeground='#FF1493',
            command=add
        )
        btn_add_enter.pack(side='bottom', anchor='s')
        if self.main.ongoing_date is None:
            btn_add_enter.configure(text='添加经期开始日期')
        else:
            btn_add_enter.configure(text='添加经期结束日期')

        box_yyyy = Combobox(frame_add, width=4, state='readonly')   #年选项框
        box_yyyy['value'] = tuple(range(2000, date.today().year + 1))
        box_yyyy.current(date.today().year - 2000)      #默认值为今天
        box_yyyy.pack(side='left', anchor='n')

        label_year = Label(frame_add, text='年  ', bg='#FFF0F5')
        label_year.pack(side='left', anchor='n')

        box_mm = Combobox(frame_add, width=2, state='readonly')     #月选项框
        box_mm['value'] = tuple(range(1, 13))
        box_mm.current(date.today().month - 1)          #默认值为今天
        box_mm.pack(side='left', anchor='n')

        label_month = Label(frame_add, text='月  ', bg='#FFF0F5')
        label_month.pack(side='left', anchor='n')

        box_dd = Combobox(frame_add, width=2, state='readonly')     #日选项框
        box_dd['value'] = tuple(range(1, 32))
        box_dd.current(date.today().day - 1)            #默认值为今天
        box_dd.pack(side='left', anchor='n')

        label_day = Label(frame_add, text='日\n\n', bg='#FFF0F5')
        label_day.pack(side='left', anchor='n')

        dialog_add.update_idletasks()   #手动更新显示，以获得布局后的窗口宽高来设置窗口位置
        dialog_add_x = int((dialog_add.winfo_screenwidth() * self.scale_factor - dialog_add.winfo_width()) / 2)
        dialog_add_y = int((dialog_add.winfo_screenheight() * self.scale_factor - dialog_add.winfo_height()) / 2)
        dialog_add.geometry('+{}+{}'.format(dialog_add_x, dialog_add_y)) #设置窗口位置
        dialog_add.resizable(False, False)      #锁定窗口大小
        dialog_add.deiconify()      #显示窗口
        # dialog_add.wait_window()

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

    def click_list(self):
        '''点击查看记录'''
        self.indicator.place(relx=0.9, rely=0.61, anchor='center')  #移动爱心位置
        self.current_frame.destroy()       #关闭当前的右侧页面
        self.init_frame_list()         #打开新的右侧页面
        self.current_frame = self.frame_list

    def click_settings(self):
        '''点击设置按钮'''
        self.indicator.place(relx=0.9, rely=0.74, anchor='center')  #移动爱心位置
        self.current_frame.destroy()       #关闭当前的右侧页面
        self.init_frame_settings()         #打开新的右侧页面
        self.current_frame = self.frame_settings

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
        heart_rain.focus_set()      #焦点切换到对话框

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
        SEPPD_FACTOR = 0.75     #下落速度系数

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
                heart_rain.move(hearts[i], 0, speed[i] * SEPPD_FACTOR)
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
        elif self.current_frame == self.frame_list:
            self.click_list()


if __name__ == '__main__':
    print('This is not the start file, please run "main.py".')