import re
import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import time


class TkGui:
    vse = "1、首先解压驱动程序(.exe)文件，得到一个文件夹。\n" \
          "2、打开File - open选择解压好的文件夹，等待修改完成。\n" \
          "3、待到提示是否启动安装的时候按提示执行即可。\n"

    def __init__(self, win):
        win.title('N卡驱动inf配置修改器')
        win.geometry('800x500')
        menubar = tk.Menu(win)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='Open', command=LogicProgram.file_path)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=win.quit)
        win.config(menu=menubar)
        file_selection = tk.Frame(win)
        file_selection.pack()

        output1 = tk.LabelFrame(win)
        output1.pack()

        na2 = tk.Label(output1, text='查找值：', width=8)
        na2.grid(column=5, row=0, sticky='n')
        va2 = tk.Entry(output1, width=80)
        va2.grid(column=6, row=0, sticky='n')

        na3 = tk.Label(output1, text='替换值：', width=8)
        na3.grid(column=5, row=1)
        va3 = tk.Entry(output1, width=80)
        va3.grid(column=6, row=1)

        output2 = tk.LabelFrame(win)
        output2.pack()

        t1 = tk.Text(output2, width=89)
        t1.pack()
        t1.insert("insert", "1、通过解压软件解压下载的.exe文件。\n")
        t1.insert("end", "2、打开 File -- open 在文件夹选择框里，选择解压好的驱动文件的文件夹。\n")
        t1.insert("end", "3、inf修改完毕后，按照提示选择是否进行安装。\n")

        t1.configure(state='disabled')
        t1.configure(state='normal')

        # tk.Label(output, text='查找和替换的值：').grid(row=1, column=0)
        # tk.Entry(output, width=80).grid(row=1, column=1)
        # tk.Label(output, text=TkGui.vse).grid()


class LogicProgram:
    path = ''
    inf_path = r'/Display.Driver/nvcvi.inf'
    a_value = r'PCI\VEN_10DE&DEV_1C60&SUBSYS_6A031558'
    b_value = r'PCI\VEN_10DE&DEV_1C60&SUBSYS_74811558'

    @staticmethod
    def file_path():
        path = filedialog.askdirectory()
        if not path:
            return
        LogicProgram.path = path
        discoloration = threading.Thread(target=LogicProgram.modification)
        discoloration.start()

    @staticmethod
    def modification():
        if not os.path.exists(LogicProgram.path + '/setup.exe'):
            messagebox.showwarning(title='错误', message='没有找到安装程序，请重新选择文件夹。')
            return
        if not os.path.exists(LogicProgram.path + LogicProgram.inf_path):
            messagebox.showwarning(title='错误', message='没有找到inf文件！请确认选择的文件夹是否正确')
            return
        infox = open(LogicProgram.path + LogicProgram.inf_path, mode='tr')
        data = infox.read()
        finds = data.find(LogicProgram.a_value)
        if finds == -1:
            messagebox.showwarning(title='错误', message='inf文件内找不到：{}'.format(LogicProgram.a_value))
            return
        data = data.replace(LogicProgram.a_value, LogicProgram.b_value)
        conserve = open(LogicProgram.path + LogicProgram.inf_path, mode='w', encoding='utf-8')
        conserve.write(data)
        conserve.close()
        if not messagebox.askokcancel(title='提示', message='inf文件修改完成，是否开始执行安装程序？'):
            return
        LogicProgram.installing_the_drive()

    @staticmethod
    def installing_the_drive():
        if os.system('bcdedit.exe /set nointegritychecks on') != 0:
            messagebox.showwarning(title='错误', message='关闭驱动签名验证失败！')
            return
        os.system(LogicProgram.path + '/setup.exe')
        if os.system('bcdedit.exe /set nointegritychecks off') != 0:
            messagebox.showwarning(title='错误', message='重新开启驱动签名验证失败')
            return


if __name__ == '__main__':
    window = tk.Tk()  # 实例化Gui库
    TkGui(window)
    LogicProgram()
    window.mainloop()
