# -*- coding:utf-8 -*-
from datetime import date
from datetime import timedelta
import sys

version = '1.0'     #版本号
records_file = 'records.csv'    #记录保存路径
ongoing_file = 'ongoing.csv'    #正在进行的经期信息
help_file = 'help_msg.txt'      #帮助信息路径


class Main():
    def __init__(self):
        print('|******************************************|')
        print('|  _   _                            _   _  |')
        print('| | | | | __ _ _ __  ___  ___ _ __ | | | | |')
        print("| | |_| |/ _` | '_ \/ __|/ _ \ '_ \| |_| | |")
        print('| |  _  | (_| | | | \__ \  __/ | | |  _  | |')
        print('| |_| |_|\__,_|_| |_|___/\___|_| |_|_| |_| |')
        print('|                                          |')
        print('|    经期计算器 Period Calculator V%s     |' % version)
        print('|                                          |')
        print('|******************************************|\n')

        self.count = 0                          #记录条数(int)
        self.average_interval = None            #总平均周期(int)
        self.average_interval_last_six = None   #近六次平均周期(int)
        self.next_date = None                   #预计下次经期开始(date)
        self.Ovulation = None                   #预计排卵日(date)
        self.average_duration = None            #平均经期持续天数(int)
        self.ongoing_date = None                #正在进行中的经期开始日期(date)
        self.records = []   #存放从文件读取的经期记录，并且加上间隔天数
        # 结构范例: （持续天数指(结束日期-开始日期+1)）
        # [{‘from_date': '2015-10-28', 'duration': 6, 'interval': None}, 
        #  {‘from_date': '2015-11-30', 'duration': 6, 'interval': 33}]

        try:
            self.load()         #从文件读取全部经期记录
            self.show_stats()   #输出统计信息
        except Exception:       #文件数据格式错误
            self.show_stats()   #已在parse_date方法中完成异常处理，因处在错误的选择分支，此处跳出语句重新执行
        self.help()
        self.menu()

    def load(self):
        #读取全部经期记录
        try:
            with open(records_file, encoding='utf-8') as file_obj:
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
            #每次记录应当时间符合顺序且没有重叠
            if self.count > 1:
                for i in range(1, len(self.records)):
                    if (self.parse_date(self.records[i - 1]['from_date']) 
                            + timedelta(self.records[i - 1]['duration'] - 1) 
                            - self.parse_date(self.records[i]['from_date'])).days >= 0:
                        raise ValueError

        except FileNotFoundError:
            print('\n未找到记录文件"%s", 已重新创建\n' % records_file)
            open(records_file, 'w', encoding='utf-8').close()       

        except (ValueError, TypeError):
            print('\n文件"%s"中的记录存在错误，无法读取' % records_file)
            print('输入"y"将创建新记录文件，输入其他内容将导致程序关闭')
            print('【警告：创建新记录文件将擦去原"' + records_file + '"中的所有信息】\n')
            if input('> ') == 'y':
                open(records_file, 'w', encoding='utf-8').close()
                self.count = 0
                print('\n记录文件"' + records_file + '"已重新创建')
            else:
                sys.exit()

        #最后一次经期的结束日期不应当在未来
        while self.count > 0:
            if (self.parse_date(self.records[-1]['from_date'])
                    - date.today()).days + self.records[-1]['duration'] - 1 > 0:
                print('\n您的最后一次经期结束于未来，继续使用须删除该条记录')
                print('输入"y"将删除最后一条记录，输入其他内容将导致程序关闭\n')
                if input('> ') == 'y':
                    del self.records[-1]
                    self.count -= 1
                    self.save()
                else:
                    sys.exit()
            else:
                break

        #读取当前进行中经期记录
        try:
            with open(ongoing_file, encoding='utf-8') as file_obj:
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
            self.ongoing_date = None
            open(ongoing_file, 'w', encoding='utf-8').close()   

    #将self.records列表中的记录保存至文件
    def save(self, filename=records_file):
        with open(filename, 'w', encoding='utf-8') as file_obj:
            for record in self.records:
                file_obj.write(record['from_date'] + ',' + str(record['duration']) + '\n')

    #计算各种统计数据
    def calculate(self):
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

    #进入循环菜单，等待命令输入
    def menu(self):
        while True:
            command = input('> ').lower()
            if command == 'exit':
                break
            elif command == 'help':
                self.help()
            elif command == 'stats':
                self.show_stats()
            elif command == 'list':
                self.show_records()
            elif command == 'future':
                self.future()
            elif command == 'del':
                self.delete()
            elif command == 'del last':
                self.delete_last()
            elif command == 'del all':
                self.delete_all()
            elif command == 'reset':
                self.reset()
            elif command == 'add':
                self.add()
            elif command == 'insert':
                self.insert()
            else:
                print('\n您输入的指令有误')
                self.help()

    #输出帮助
    def help(self):
        try:
            with open(help_file, encoding='utf-8') as help_file_obj:
                help_msg = help_file_obj.read().rstrip()
                print('\n' + help_msg + '\n')
        except FileNotFoundError:
            print('\n找不到文件"' + help_file + '"\n')

    #输出统计数据
    def show_stats(self):
        self.calculate()
        print('\n今天是{}年{}月{}日'.format(date.today().year, date.today().month, 
                date.today().day))
        print('您当前一共有%d条记录' % self.count)
        if self.count > 1:
            print('------------------------------------------')
            print('近6次平均周期:\t%d天' % self.average_interval_last_six)
            print('平均周期:     \t%d天' % self.average_interval)
            print('平均经期持续: \t%d天' % self.average_duration)
            if self.ongoing_date is None:
                print('可能的排卵日: \t{}年{}月{}日'.format(self.Ovulation.year, 
                        self.Ovulation.month, self.Ovulation.day))
                diff = (self.next_date - date.today()).days
                if diff >= 0:
                    print('预计下次来临: \t{}年{}月{}日，距今还有{}天'.format(self.next_date.year, 
                            self.next_date.month, self.next_date.day, diff))
                else:
                    print('预计下次来临: \t{}年{}月{}日，距今已过去{}天'.format(self.next_date.year, 
                            self.next_date.month, self.next_date.day, -diff))
        if self.ongoing_date is not None:
            ongoing_duration = (date.today() - self.ongoing_date).days + 1
            print('------------------------------------------')
            print('您当前处于经期第%d天 ' % ongoing_duration, end='')
            print('（开始于{}年{}月{}日）'.format(self.ongoing_date.year, 
                            self.ongoing_date.month, self.ongoing_date.day))
        print('')

    #显示全部记录
    def show_records(self):
        self.calculate()
        print('\n------------------------------------')
        print('序号\t起始日期  持续天数  间隔天数')
        print('------------------------------------')
        for i in range(self.count):
            print('{}\t{}\t{}\t{}'.format(i+1, self.records[i]['from_date'], 
                    self.records[i]['duration'], self.records[i]['interval']))
        print('------------------------------------')
        if self.count == 0:
            print('当前还没有任何记录哦，赶紧来添加吧！')
        print('')

    #输出未来五次经期预测
    def future(self):
        self.calculate()
        if self.count > 1:
            print('\n未来5次经期的起始日期预测: ')
            if self.ongoing_date is not None:   #从当前进行中经期往后算
                future_date = self.ongoing_date
            else:                               #从最后一次记录往后算
                future_date = self.parse_date(self.records[-1]['from_date'])
            for i in range(5):
                future_date += timedelta(self.average_interval_last_six)
                print('\t', end='')
                print(future_date)
            print('')
        else:
            print('\n记录太少啦，暂时无法进行预测\n')

    #删除某条记录
    def delete(self):    
        if self.count > 0:
            self.show_records()
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

    #删除最后一条记录
    def delete_last(self):
        if self.count > 0:
            self.show_records()
            print('\n请输入"y"确认删除最后一条记录\n')
            if input('> ') == 'y':
                del self.records[-1]
                self.count -= 1
                self.save()
                print('\n已删除最后一条记录\n')
            else:
                print('\n已取消，没有任何记录被删除\n')
        else:
            print('\n删除失败，当前还没有任何记录哦\n')

    #删除全部记录
    def delete_all(self):
        if self.count > 0:
            self.show_records()
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

    #删除正在进行中的经期
    def reset(self):
        self.ongoing_date = None
        open(ongoing_file, 'w', encoding='utf-8').close()
        print('\n已清除正在进行中的经期\n')

    #记录经期开始/结束
    def add(self):
        #还没有进行中的经期
        if self.ongoing_date is None:
            print('\n正在记录经期开始...\n')
            print('请输入选项: ')
            print('1 今天开始    2 其他日期    3 取消\n')
            option = input('> ').lower()
            if option == '1':
                self.ongoing_date = date.today()
                with open(ongoing_file, 'w', encoding='utf-8') as file_obj:
                    file_obj.write('{},{},{}'.format(self.ongoing_date.year, 
                            self.ongoing_date.month, self.ongoing_date.day))
                print('今天是经期第一天\n')
            elif option == '2':
                try:
                    print('\n正在输入经期开始日期...')
                    yyyy = int(input('请输入年: '))
                    mm = int(input('请输入月: '))
                    dd = int(input('请输入日: '))
                    date_to_start = date(yyyy, mm, dd)
                    if (date.today() - date_to_start).days < 0:
                        print('\n已取消————不能记录未来的经期哦！\n')
                    elif self.count > 0 and (self.parse_date(self.records[-1]['from_date']) 
                                        + timedelta(self.records[-1]['duration'] - 1) 
                                        - date_to_start).days >= 0:
                        print('\n已取消————不能在上一次经期结束前开始！\n')
                    else:
                        self.ongoing_date = date_to_start
                        with open(ongoing_file, 'w', encoding='utf-8') as file_obj:
                            file_obj.write('{},{},{}'.format(date_to_start.year, 
                                    date_to_start.month, date_to_start.day))
                        print('\n记录成功 ({})\n'.format(self.ongoing_date))
                except ValueError:
                    print('\n您输入的日期有误，已取消\n')
            else:
                print('\n操作取消，已返回主菜单\n')
 
        #已有进行中的经期
        else:
            print('\n正在记录经期结束（结束日期指经期最后一天当天）...')
            print('注：如果您需要记录经期开始，请先取消，再输入"reset"移除正在进行的经期\n')
            print('请输入选项: ')
            print('1 今天结束    2 其他日期    3 取消\n')
            option = input('> ').lower()
            if option == '1':
                yyyy = date.today().year
                mm = date.today().month
                dd = date.today().day
                duration = (date.today() - self.ongoing_date).days + 1
                self.records.append({'from_date': '{}-{:0>2d}-{:0>2d}'.
                        format(self.ongoing_date.year, self.ongoing_date.month, 
                        self.ongoing_date.day), 'duration': duration, 'interval': None})
                self.count += 1
                self.save()
                self.ongoing_date = None        #清除进行中的经期
                open(ongoing_file, 'w', encoding='utf-8').close()
                print('\n今天经期结束啦\n')
            elif option == '2':
                try:
                    print('\n正在输入经期结束日期...')
                    yyyy = int(input('请输入年: '))
                    mm = int(input('请输入月: '))
                    dd = int(input('请输入日: '))
                    date_to_end = date(yyyy, mm, dd)
                    duration = (date_to_end - self.ongoing_date).days + 1
                    if (date.today() - date_to_end).days < 0:
                        print('\n已取消————不能穿越到未来哦！\n')
                    elif duration < 1:
                        print('\n已取消————经期不能在开始前就结束哦！\n')
                    else:
                        self.records.append({'from_date': '{}-{:0>2d}-{:0>2d}'.
                                                format(self.ongoing_date.year, 
                                                    self.ongoing_date.month, 
                                                    self.ongoing_date.day), 
                                            'duration': duration, 
                                            'interval': None})
                        self.count += 1
                        self.save()
                        self.ongoing_date = None        #清除进行中的经期
                        open(ongoing_file, 'w', encoding='utf-8').close()
                        print('\n已记录经期结束\n')  
                except ValueError:
                    print('\n您输入的日期有误，已取消\n')
            else:
                print('\n操作取消，已返回主菜单\n')

    #插入一条完整记录        
    def insert(self):
        if self.count > 0:
            self.show_records()
            print('正在插入记录...')
            print('注意: 原位置及其后的记录将向后移动一行，间隔天数也会随之改变\n')
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
                self.records.insert(0, {'from_date': '{}-{:0>2d}-{:0>2d}'.
                                                format(date_to_start.year, 
                                                    date_to_start.month, 
                                                    date_to_start.day), 
                                            'duration': duration, 
                                            'interval': None})
                self.count += 1
                self.save()
                print('\n已成功添加记录\n')

    #辅助函数，将日期字符串转变为date对象
    def parse_date(self, s):
        try:
            yyyy, mm, dd = s.split('-')
            return date(int(yyyy), int(mm), int(dd))
        except (ValueError, TypeError):
            print('文件"%s"中的记录存在错误，无法读取' % records_file)
            print('输入"y"将创建新记录文件，输入其他内容将导致程序关闭')
            print('【警告：创建新记录文件将擦去原"' + records_file + '"中的所有信息】\n')
            if input('> ') == 'y':
                open(records_file, 'w', encoding='utf-8').close()
                self.count = 0
                print('\n记录文件"' + records_file + '"已重新创建')
            else:
                sys.exit()


'''程序入口'''
if __name__ == '__main__':
    main = Main()