# -*- coding:utf-8 -*-
from datetime import date
from datetime import timedelta
from user_interface import UserInterface
import os
import json

version = '2.0'     #版本号

class Main():
    '''程序核心，包括初始化与功能逻辑'''

    def __init__(self):
        self.version = version
        self.records_file = 'records.csv'    #默认记录保存位置
        self.ongoing_file = 'ongoing.csv'    #默认正在进行的经期信息保存位置
        self.window_width = 600     #默认窗口宽
        self.window_height = 600    #默认窗口高
        self.dpi_adapt = True       #默认开启高分屏缩放适配
        
        try:    #加载设置
            with open('config.json') as file_obj:
                settings = json.load(file_obj)
                self.records_file = settings['records_file']
                self.ongoing_file = settings['ongoing_file']
                self.window_width = settings['window_width']
                self.window_height = settings['window_height']
                self.dpi_adapt = settings['dpi_adapt']
        except FileNotFoundError:
            self.save_settings()

        self.load_error = False                 #文件读取是否异常（决定是否弹窗警告）
        self.add_error = False                  #添加记录是否异常（决定是否弹窗警告）
        self.count = 0                          #记录条数(int)
        self.average_interval = None            #总平均周期(int)
        self.average_interval_last_six = None   #近六次平均周期(int)
        self.next_date = None                   #预计下次经期开始(date)
        self.Ovulation = None                   #预计排卵日(date)
        self.average_duration = None            #平均经期持续天数(int)
        self.ongoing_date = None                #正在进行中的经期开始日期(date)
        self.records = []                       #存放从文件读取的经期记录，并且加上间隔天数
        # 结构范例: （持续天数指(结束日期-开始日期+1)）
        # [{‘from_date': '2015-10-28', 'duration': 6, 'interval': None}, 
        #  {‘from_date': '2015-11-30', 'duration': 6, 'interval': 33}]

        self.load()         #从文件读取全部经期记录
        ui = UserInterface(self)    #启动图形界面
        ui.window.mainloop()

    def save_settings(self):
        '''保存设置'''
        settings = {}
        settings['records_file'] = self.records_file
        settings['ongoing_file'] = self.ongoing_file
        settings['window_width'] = self.window_width
        settings['window_height'] = self.window_height
        settings['dpi_adapt'] = self.dpi_adapt
        with open('config.json', 'w') as file_obj:
            json.dump(settings, file_obj, indent=4)

    def load(self):
        '''读取经期记录文件'''
        try:
            with open(self.records_file, encoding='utf-8') as file_obj:
                raw_records = file_obj.read().rstrip()  #去除尾部多余空行（如有）
                if raw_records != '':
                    for line in raw_records.split('\n'):
                        from_date, duration = line.rstrip().split(',')
                        #持续天数不应小于1天
                        if int(duration) < 1:
                            raise ValueError
                        self.records.append({'from_date': from_date, 
                                            'duration': int(duration), 
                                            'interval': None})
                        self.count += 1
            #每次记录应当日期符合顺序且没有重叠
            if self.count > 1:
                for i in range(1, len(self.records)):
                    if (self.parse_date(self.records[i - 1]['from_date']) 
                            + timedelta(self.records[i - 1]['duration'] - 1) 
                            - self.parse_date(self.records[i]['from_date'])).days >= 0:
                        raise DateLogicError
            #最后一次经期的结束日期不应当在未来
            if self.count > 0 and (self.parse_date(self.records[-1]['from_date'])
                    - date.today()).days + self.records[-1]['duration'] - 1 > 0:
                raise DateLogicError

        except FileNotFoundError:
            #找不到记录文件
            open(self.records_file, 'w', encoding='utf-8').close()  #新建     

        except (ValueError, TypeError):
            #记录文件有错误
            self.load_error = True
            self.file_rename = 'old_' + self.records_file   #重命名目标文件名
            while True:
                if os.path.exists(self.file_rename):
                    self.file_rename = 'old_' + self.file_rename
                else:
                    break
            os.rename(self.records_file, self.file_rename)  #重命名
            open(self.records_file, 'w', encoding='utf-8').close()  #新建
            self.records = []
            self.count = 0
            self.error_msg = '记录文件"{}"存在格式错误, 已重新创建！\n原记录文件已备份为"{}"'.\
                    format(self.records_file, self.file_rename)

        except DateLogicError:
            #日期逻辑错误
            self.load_error = True
            self.file_rename = 'old_' + self.records_file   #重命名目标文件名
            while True:
                if os.path.exists(self.file_rename):
                    self.file_rename = 'old_' + self.file_rename
                else:
                    break
            os.rename(self.records_file, self.file_rename)  #重命名
            open(self.records_file, 'w', encoding='utf-8').close()  #新建
            self.records = []
            self.count = 0
            self.error_msg = '记录文件"{}"内存在日期逻辑错误, 已重新创建！\n原记录文件已备份为"{}"'.\
                    format(self.records_file, self.file_rename)

        #读取当前进行中经期记录
        try:
            with open(self.ongoing_file, encoding='utf-8') as file_obj:
                raw_ongoing = file_obj.read().rstrip()
                if raw_ongoing != '':
                    yyyy, mm, dd = raw_ongoing.split(',')
                    self.ongoing_date = date(int(yyyy), int(mm), int(dd))
                    #经期开始应当不晚于今天
                    if (date.today() - self.ongoing_date).days < 0:
                        raise ValueError
                    #经期开始应当晚于最后一条记录的结束日期
                    if self.count > 0:
                        last_end_date = self.parse_date(self.records[-1]['from_date']) \
                                        + timedelta(self.records[-1]['duration'] - 1)
                        if (last_end_date - self.ongoing_date).days >= 0:
                            raise ValueError
        except (FileNotFoundError, ValueError, TypeError):
            #进行中经期的记录文件不存在或存在错误
            self.ongoing_date = None
            open(self.ongoing_file, 'w', encoding='utf-8').close()

    def save(self):
        '''将self.records列表中的记录保存至文件'''
        filename = self.records_file
        with open(filename, 'w', encoding='utf-8') as file_obj:
            for record in self.records:
                file_obj.write(record['from_date'] + ',' + str(record['duration']) + '\n')

    def calculate(self):
        '''计算各种统计数据'''
        #计算每次间隔天数
        if self.count > 1:
            for i in range(1, self.count):
                interval = self.parse_date(self.records[i]['from_date']) \
                             - self.parse_date(self.records[i-1]['from_date'])
                self.records[i]['interval'] = interval.days

        #计算平均周期
        if self.count > 1:
            intervals_sum = 0
            for i in range(1, self.count):
                intervals_sum += self.records[i]['interval']
            self.average_interval = round(intervals_sum / (self.count - 1))

        #计算最近6次平均周期（记录不足则按全部记录来算）
        if self.count > 1:
            intervals_sum = 0
            i = self.count - 1
            while (i > 0) and (i > self.count - 7):
                intervals_sum += self.records[i]['interval']
                i -= 1
            self.average_interval_last_six = round(intervals_sum / (self.count - 1 - i))

        #计算平均经期持续天数
        if self.count > 0:
            duration_sum = 0
            for record in self.records:
                duration_sum += record['duration']
            self.average_duration = round(duration_sum / self.count)

        #计算下次经期预计开始日期
        if self.count > 1:
            self.next_date = self.parse_date(self.records[-1]['from_date']) \
                            + timedelta(self.average_interval_last_six)

        #计算下次经期前预计排卵日
        if self.count > 1:
            self.Ovulation = self.next_date - timedelta(14)

    def show_stats(self):
        '''输出统计数据'''
        self.calculate()
        self.print_ongoing = ('今天是{}年{}月{}日\n\n'.format(date.today().year, 
                date.today().month, date.today().day))
        if self.ongoing_date is not None:
            ongoing_duration = (date.today() - self.ongoing_date).days + 1
            self.print_ongoing += ('经期第%d天' % ongoing_duration)
            self.print_ongoing += ('（开始于{}月{}日）'.format(self.ongoing_date.month, 
                    self.ongoing_date.day))

        self.print_stats = ('\n您当前一共有%d条记录\n' % self.count)
        if self.count > 1:
            self.print_stats += ('----------------------------\n')
            self.print_stats += ('近6次平均周期:\t%d天\n' % self.average_interval_last_six)
            self.print_stats += ('平均周期:     \t%d天\n' % self.average_interval)
            self.print_stats += ('平均经期持续: \t%d天\n' % self.average_duration)
            if self.ongoing_date is None:
                self.print_stats += ('可能的排卵日: \t{}年{}月{}日\n'.format(self.Ovulation.year, 
                        self.Ovulation.month, self.Ovulation.day))
                diff = (self.next_date - date.today()).days
                if diff >= 0:
                    self.print_stats += ('预计下次来临: \t{}年{}月{}日\n\t\t（距今还有{}天）\n'.format(
                            self.next_date.year, self.next_date.month, self.next_date.day, diff))
                else:
                    self.print_stats += ('预计下次来临: \t{}年{}月{}日\n\t\t（距今已过去{}天）\n'.format(
                            self.next_date.year, self.next_date.month, self.next_date.day, -diff))
        self.future()

    def future(self):
        '''输出未来五次经期预测'''
        self.print_future = ''
        if self.count > 1:
            self.print_future += ('\n未来5次经期的起始日期预测: \n')
            if self.ongoing_date is not None:   #从当前进行中经期往后算
                future_date = self.ongoing_date
            else:                               #从最后一次记录往后算
                future_date = self.parse_date(self.records[-1]['from_date'])
            for i in range(5):
                future_date += timedelta(self.average_interval_last_six)
                self.print_future += ('\n    ')
                self.print_future += (future_date.isoformat())
    
    def show_list(self):
        '''列出记录'''
        self.calculate()
        self.print_list = []
        for i in range(self.count):
            self.print_list.append('{:>3}    {:>10}    {}    {}'.format(
                i+1, 
                self.records[i]['from_date'], 
                self.records[i]['duration'], 
                self.records[i]['interval']
            ))

    def delete(self):
        '''施工中''''''删除某条记录'''
        if self.count > 0:
            
            try:
                index = int(input('请输入您想要删除的记录序号: ')) - 1
                print('\n请输入"y"确认，注意随后的间隔天数会相应改变\n')
                if input('> ') == 'y':
                    del self.records[index]
                    self.count -= 1
                    self.save()
                    print('\n已删除您选择的记录\n')
                else:
                    print('\n已取消，没有任何记录被删除\n')
            except (IndexError, ValueError):
                print('\n您输入的序号无效，没有任何记录被删除\n')
        else:
            print('\n删除失败，当前还没有任何记录哦\n')

    def delete_all(self):
        '''施工中''''''删除全部记录'''
        if self.count > 0:
            print('【警告！所有记录将被删除】\n请输入"Yes"确认该操作\n')
            if input('> ') == 'Yes':
                self.save(filename='records.bak')
                self.records = []
                self.count = 0
                self.save()
                print('\n已删除全部记录\n')
            else:
                print('\n已取消，没有任何记录被删除\n')
        else:
            print('\n删除失败，当前还没有任何记录哦\n')

    def reset(self):
        '''删除正在进行中的经期'''
        self.ongoing_date = None
        open(self.ongoing_file, 'w', encoding='utf-8').close()

    def add(self, yyyy, mm, dd):
        '''记录经期开始/结束'''
        #还没有进行中的经期
        if self.ongoing_date is None:
            try:
                date_to_start = date(yyyy, mm, dd)
                if (date.today() - date_to_start).days < 0:
                    self.add_error = True
                    self.error_msg = '不能穿越到未来哦！'
                elif self.count > 0 and (self.parse_date(self.records[-1]['from_date']) 
                                    + timedelta(self.records[-1]['duration'] - 1) 
                                    - date_to_start).days >= 0:
                    self.add_error = True
                    self.error_msg = '不能早于上一次经期哦！\n如果需要增添或修改历史记录清'
                else:
                    self.ongoing_date = date_to_start
                    with open(self.ongoing_file, 'w', encoding='utf-8') as file_obj:
                        file_obj.write('{},{},{}'.format(date_to_start.year, 
                                date_to_start.month, date_to_start.day))
                    self.add_error = False          #添加记录成功
            except ValueError:
                self.add_error = True
                self.error_msg = '该日期有误！'
 
        #已有进行中的经期
        else:
            try:
                date_to_end = date(yyyy, mm, dd)
                duration = (date_to_end - self.ongoing_date).days + 1
                if (date.today() - date_to_end).days < 0:
                    self.add_error = True
                    self.error_msg = '不能穿越到未来哦！'
                elif duration < 1:
                    self.add_error = True
                    self.error_msg = '经期不能在开始前就结束哦！'
                else:
                    self.records.append({
                        'from_date': '{}-{:0>2d}-{:0>2d}'.format(
                            self.ongoing_date.year, 
                            self.ongoing_date.month, 
                            self.ongoing_date.day
                        ), 
                        'duration': duration, 
                        'interval': None
                    })
                    self.count += 1
                    self.save()
                    self.ongoing_date = None        #清除进行中的经期
                    open(self.ongoing_file, 'w', encoding='utf-8').close()
                    self.add_error = False          #添加记录成功
            except ValueError:
                self.add_error = True
                self.error_msg = '该日期有误！'

    def insert(self):
        '''施工中''''''插入一条完整记录'''
        if self.count > 0:

            flag = True

            try:
                index = int(input('请输入您想要插入记录的位置序号: ')) - 1
                if index > (self.count) or index < 0:
                    raise IndexError
            except (IndexError, ValueError):
                flag = False
                print('\n您输入的序号无效，已返回主菜单\n')

            if flag:
                try:
                    print('\n请输入开始日期...')
                    yyyy = int(input('请输入年: '))
                    mm = int(input('请输入月: '))
                    dd = int(input('请输入日: '))
                    date_to_start = date(yyyy, mm, dd)
                    if index > 0 and (self.parse_date(self.records[index - 1]['from_date']) 
                                + timedelta(self.records[index - 1]['duration'] - 1) 
                                - date_to_start).days >= 0:
                        flag = False
                        print('\n已取消————不能在前一次经期结束前开始！\n')
                    elif (date.today() - date_to_start).days < 0:
                        flag = False
                        print('\n已取消————不能记录未来的经期哦！\n')
                    elif self.ongoing_date is not None and (date_to_start - 
                            self.ongoing_date).days >= 0:
                        flag = False
                        print('\n已取消————开始日期应早于进行中的经期的开始日期！\n')
                except ValueError:
                    flag = False
                    print('\n您输入的日期有误，已取消\n')
            
            if flag:
                try:
                    print('\n请输入结束日期...')
                    yyyy = int(input('请输入年: '))
                    mm = int(input('请输入月: '))
                    dd = int(input('请输入日: '))
                    date_to_end = date(yyyy, mm, dd)
                    duration = (date_to_end - date_to_start).days + 1
                    if index < self.count and (date_to_end - 
                            self.parse_date(self.records[index]['from_date'])).days >= 0:
                        flag = False
                        print('\n已取消————结束应早于下一次经期记录的开始日期！\n')
                    elif (date.today() - date_to_end).days < 0:
                        flag = False
                        print('\n已取消————不能穿越到未来哦！\n')
                    elif duration < 1:
                        flag = False
                        print('\n已取消————经期不能在开始前就结束哦！\n')
                    elif self.ongoing_date is not None and (date_to_end - 
                            self.ongoing_date).days >= 0:
                        flag = False
                        print('\n已取消————结束应早于进行中的经期的开始日期！\n')
                except ValueError:
                    flag = False
                    print('\n您输入的日期有误，已取消\n')

            #已满足约束条件，修改self.records和文件
            if flag:
                self.records.insert(index, {'from_date': '{}-{:0>2d}-{:0>2d}'.
                                                format(date_to_start.year, 
                                                    date_to_start.month, 
                                                    date_to_start.day), 
                                            'duration': duration, 
                                            'interval': None})
                self.count += 1
                self.save()
                print('\n已成功添加记录\n')

        #记录条数尚位0时
        else:
            print('正在添加您的第一条记录...\n')
            flag = True

            try:
                print('\n请输入开始日期...')
                yyyy = int(input('请输入年: '))
                mm = int(input('请输入月: '))
                dd = int(input('请输入日: '))
                date_to_start = date(yyyy, mm, dd)
                if (date.today() - date_to_start).days < 0:
                    flag = False
                    print('\n已取消————不能记录未来的经期哦！\n')
                elif self.ongoing_date is not None and (date_to_start - 
                        self.ongoing_date).days >= 0:
                    flag = False
                    print('\n已取消————开始日期应早于进行中的经期的开始日期！\n')
            except ValueError:
                flag = False
                print('\n您输入的日期有误，已取消\n')

            if flag:
                try:
                    print('\n请输入结束日期...')
                    yyyy = int(input('请输入年: '))
                    mm = int(input('请输入月: '))
                    dd = int(input('请输入日: '))
                    date_to_end = date(yyyy, mm, dd)
                    duration = (date_to_end - date_to_start).days + 1
                    if (date.today() - date_to_end).days < 0:
                        flag = False
                        print('\n已取消————不能穿越到未来哦！\n')
                    elif duration < 1:
                        flag = False
                        print('\n已取消————经期不能在开始前就结束哦！\n')
                    elif self.ongoing_date is not None and (date_to_end - 
                            self.ongoing_date).days >= 0:
                        flag = False
                        print('\n已取消————结束应早于进行中的经期的开始日期！\n')
                except ValueError:
                    flag = False
                    print('\n您输入的日期有误，已取消\n')

            #已满足约束条件，修改self.records和文件
            if flag:
                self.records.insert(0, {
                    'from_date': '{}-{:0>2d}-{:0>2d}'.format(
                        date_to_start.year, 
                        date_to_start.month, 
                        date_to_start.day
                    ), 
                    'duration': duration, 
                    'interval': None
                })
                self.count += 1
                self.save()
                print('\n已成功添加记录\n')

    def parse_date(self, s):
        '''辅助函数，将日期字符串转变为date对象'''
        yyyy, mm, dd = s.split('-')
        return date(int(yyyy), int(mm), int(dd))

class DateLogicError(Exception):
    '''日期逻辑异常类'''
    pass


'''程序入口'''
if __name__ == '__main__':
    main = Main()