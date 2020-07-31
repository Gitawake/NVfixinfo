import re
import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import time


class Config:
    inf_name = r'/Display.Driver/nvcvi.inf'
    a_file_path = ''
    Original_value = r'PCI\VEN_10DE&DEV_1C60&SUBSYS_6A031558'
    Replacement_value = r'PCI\VEN_10DE&DEV_1C60&SUBSYS_74811558'
    winrar = r'"c:/Program Files/WinRAR/WinRAR.exe"'
    w = 800
    h = 500


window = tk.Tk()  # 实例化Gui库

window.title('N卡驱动inf配置修改器')  # 定义ui窗口标题

window.geometry(f'{Config.w}x{Config.h}')  # 定义ui窗口大小


# def callbackClose():
#     os.system('bcdedit.exe /set nointegritychecks off')
#     messagebox.showwarning(title='提示', message='关闭程序并且重新开启驱动强制签名')
#     sys.exit(0)
#
#
# window.protocol("WM_DELETE_WINDOW", callbackClose)


def file_path():
    Config.a_file_path = filedialog.askopenfilename()
    if Config.a_file_path != '':
        # 定义一个线程用于抽奖中的效果
        discoloration = threading.Thread(target=modification)
        # 运行线程
        discoloration.start()


def installing_the_drive():
    tk.Label(output, text='开始执行禁止驱动强制签名命令', wraplength=Config.w).grid(column=1, sticky='W')
    if os.system('bcdedit.exe /set nointegritychecks on') == 0:
        tk.Label(output, text='操作成功完成。', wraplength=Config.w).grid(column=1, sticky='W')
        os.system(r'C:\Users\Administrator\Downloads\445.75-notebook-win10-64bit-international-dch-whql\setup.exe')
        tk.Label(output, text='安装进程结束，重新开启驱动强制签名', wraplength=Config.w).grid(column=1, sticky='W')
        if os.system('bcdedit.exe /set nointegritychecks off') == 0:
            tk.Label(output, text='操作成功完成。', wraplength=Config.w).grid(column=1, sticky='W')
        else:
            tk.Label(output, text='开启驱动强制签名失败', wraplength=Config.w).grid(column=1, sticky='W')
    else:
        tk.Label(output, text='禁用驱动强制签名失败，请开启禁用驱动签名模式后手动执行解压出来的驱动进行安装！', wraplength=Config.w).grid(column=1, sticky='W')


menubar = tk.Menu(window)

filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)

filemenu.add_command(label='Open', command=file_path)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=window.quit)

window.config(menu=menubar)

file_selection = tk.Frame(window)  # 创建一个frame用于放置按钮

file_selection.pack()  # 定义frame排列方式

output = tk.LabelFrame(window, text="log", labelanchor="n")  # 创建一个frame用于放置按钮

output.pack()  # 定义frame排列方式


def modification():
    if Config.a_file_path.endswith('.exe'):  # 判断文件格式
        tk.Label(output, text='开始解压文件...', wraplength=Config.w).grid(column=1, sticky='W')
        b_file_path = Config.a_file_path.replace('/', '\\')  # cmd命令需要反斜杠，所以把文件目录斜杠替换掉

        c_file_path = Config.a_file_path.rfind('.')  # 从右到左定位对应字符所在位置
        c_file_path = Config.a_file_path[:c_file_path]  # 按指定位置截取字符串获得一个用来储存解压的文件夹

        tk.Label(output, text='创建文件夹用于存放解压的驱动文件：{}'.format(c_file_path), wraplength=Config.w).grid(column=1, sticky='W')
        if not os.path.exists(c_file_path):  # 如果文件夹不存在
            os.makedirs(c_file_path)  # 创建文件夹

        command = '{} x {} * {}'.format(Config.winrar, b_file_path, c_file_path)  # 组合cmd命令
        tk.Label(output, text='开始执行解压命令：{}'.format(command), wraplength=Config.w, justify='left').grid(column=1,
                                                                                                       sticky='W')
        os.system(command)  # 执行cmd命令

        d_file_path = c_file_path + Config.inf_name
        tk.Label(output, text='查找inf文件：{}'.format(d_file_path), wraplength=Config.w).grid(column=1, sticky='W')
        if re.search(Config.inf_name, d_file_path):
            tk.Label(output, text='找到：{}'.format(d_file_path), wraplength=Config.w).grid(column=1, sticky='W')

            tk.Label(output, text='开始编辑：{}'.format(d_file_path), wraplength=Config.w).grid(column=1, sticky='W')
            infox = open(d_file_path, mode='tr')
            data = infox.read()
            tk.Label(output, text='查找inf文件内容：{}'.format(Config.Original_value), wraplength=Config.w).grid(column=1,
                                                                                                          sticky='W')
            finds = data.find(Config.Original_value)
            if finds != -1:
                data = data.replace(Config.Original_value, Config.Replacement_value)
                conserve = open(d_file_path, mode='w', encoding='utf-8')
                conserve.write(data)
                conserve.close()
                tk.Label(output, text='找到：{}，替换为：{}'.format(Config.Original_value, Config.Replacement_value),
                         wraplength=Config.w).grid(column=1, sticky='W')

                def installx():
                    # 定义一个线程用于抽奖中的效果
                    discoloration = threading.Thread(target=installing_the_drive)
                    # 运行线程
                    discoloration.start()

                tk.Button(output, text="点击开始安装驱动", command=installx).grid(column=1)
            else:
                tk.Label(output, text='inf文件内找不到：{}'.format(Config.Original_value), wraplength=Config.w).grid(column=1,
                                                                                                              sticky='W')
        else:
            tk.Label(output, text='没有找到inf文件！请确认选择的文件夹是否正确', wraplength=Config.w).grid(column=1, sticky='W')
    else:
        messagebox.showwarning(title='错误', message='文件格式不正确，请重新选择。')


window.mainloop()
