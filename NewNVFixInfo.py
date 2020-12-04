#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox


class Application(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master)
        self.logic_script = LogicScript()
        self.master = master
        self.pack()

        self.set_value = tk.Frame(self)
        self.set_value.pack()

        self.out_log = tk.Frame(self)
        self.out_log.pack()

        self.control = tk.Frame(self)
        self.control.pack()

        self.value1 = tk.Frame(self.set_value)
        self.value1.pack()

        self.value2 = tk.Frame(self.set_value)
        self.value2.pack()

        self.name_1 = tk.Label(self.value1, text="value1:", fg="red")
        self.name_1.pack(side="left")
        self.value_1 = tk.Entry(self.value1, fg="red", width='60')
        self.value_1.pack(side="right")

        self.name_2 = tk.Label(self.value2, text="value2:", fg="red")
        self.name_2.pack(side="left")
        self.value_2 = tk.Entry(self.value2, fg="red", width='60')
        self.value_2.pack(side="right")

        self.a_value = R'PCI\VEN_10DE&DEV_1C60&SUBSYS_6A031558'
        self.b_value = R'PCI\VEN_10DE&DEV_1C60&SUBSYS_74811558'
        self.value_1.insert(0, self.a_value)
        self.value_2.insert(0, self.b_value)

        self.log = tk.Text(self.out_log, width=89)
        self.sb = tk.Scrollbar(self.out_log)

        self.log.pack(side="left", fill='x')
        self.log.config(yscrollcommand=self.sb.set)

        self.sb.pack(side="right", fill='y')
        self.sb.config(command=self.log.yview_moveto(1.0))

        self.button_start = tk.Button(self.control, text="启动", fg="red", command=self.logic_script.file_path)
        self.button_start.pack(side="left")
        self.button_close = tk.Button(self.control, text="关闭", fg="red", command=self.master.destroy)
        self.button_close.pack(side="right")

    def create_widgets(self, index, chars):
        self.log.configure(state='normal')
        self.log.insert(index, chars)
        self.log.see('end')
        self.log.update()
        self.log.configure(state='disabled')

    def get_value1(self):
        value = self.value_1.get()
        return value

    def get_value2(self):
        value = self.value_2.get()
        return value


class LogicScript:

    def __init__(self):
        self.path = ''
        self.discoloration = None
        self.inf_path = R'/Display.Driver/nvcvi.inf'

    def file_path(self):
        self.path = filedialog.askdirectory()
        if not self.path:
            return
        self.discoloration = threading.Thread(target=self.modification)
        self.discoloration.start()
        app.create_widgets("insert", "开始运行修改脚本\n")

    def modification(self):
        if not os.path.exists(self.path + '/setup.exe'):
            app.create_widgets("insert", "没有找到安装程序，请重新选择文件夹\n")
            return
        app.create_widgets("insert", "找到安装程序\n")
        if not os.path.exists(self.path + self.inf_path):
            app.create_widgets("insert", "没有找到inf文件！请确认选择的文件夹是否正确\n")
            return
        app.create_widgets("insert", "找到inf文件\n")
        infox = open(self.path + self.inf_path, mode='tr')
        app.create_widgets("insert", "读取inf文件\n")
        data = infox.read()
        finds = data.find(app.get_value1())

        app.create_widgets("insert", "查找到：{}\n".format(app.get_value1()))
        if finds == -1:
            app.create_widgets("insert", "inf文件内找不到：{}\n".format(app.get_value1()))
            return
        data = data.replace(app.get_value1(), app.get_value2())
        conserve = open(self.path + self.inf_path, mode='w', encoding='utf-8')
        conserve.write(data)
        app.create_widgets("insert", "替换：{} ==> {}\n".format(app.get_value1(), app.get_value2()))
        conserve.close()
        app.create_widgets("insert", "保存修改\n")
        if not messagebox.askokcancel(title='提示', message='inf文件修改完成，是否开始执行安装程序？'):
            return
        self.installing_the_drive()

    def installing_the_drive(self):
        if os.system('bcdedit.exe /set nointegritychecks on') != 0:
            app.create_widgets("insert", "关闭驱动签名验证失败\n")
            return
        app.create_widgets("insert", "关闭驱动签名验证成功\n")
        os.system(self.path + '/setup.exe')
        if os.system('bcdedit.exe /set nointegritychecks off') != 0:
            app.create_widgets("insert", "重新开启驱动签名验证失败\n")
            return
        app.create_widgets("insert", "重新开启驱动签名验证成功\n")


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

