#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox


class Application(tk.Frame):

    def __init__(self, master=None):
        self.value = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0,)

        super().__init__(master)
        self.master = master
        self.pack()

        self.fm = tk.Frame(self)
        self.fm.pack()

        self.fm1 = tk.Frame(self)
        self.fm1.pack()

        self.log = tk.Text(self.fm, width=45, height=5)
        self.sb = tk.Scrollbar(self.fm)

        self.log.pack(side="left", fill='x')
        self.log.config(yscrollcommand=self.sb.set)

        self.sb.pack(side="right", fill='y')
        self.sb.config(command=self.log.yview_moveto(1.0))

        # self.quit = tk.Button(self.fm1, text="AC", fg="red", width=10)
        # self.quit.grid(column=0, row=0)
        # self.quit = tk.Button(self.fm1, text="%", fg="red", width=10)
        # self.quit.grid(column=1, row=0)
        # self.quit = tk.Button(self.fm1, text="/", fg="red", width=10)
        # self.quit.grid(column=3, row=0)
        #
        # self.quit = tk.Button(self.fm1, text="1", fg="red", width=10)
        # self.quit.grid(column=0, row=1)
        # self.quit = tk.Button(self.fm1, text="2", fg="red", width=10)
        # self.quit.grid(column=1, row=1)
        # self.quit = tk.Button(self.fm1, text="3", fg="red", width=10)
        # self.quit.grid(column=2, row=1)
        # self.quit = tk.Button(self.fm1, text="*", fg="red", width=10)
        # self.quit.grid(column=3, row=1)
        #
        # self.quit = tk.Button(self.fm1, text="4", fg="red", width=10)
        # self.quit.grid(column=0, row=2)
        # self.quit = tk.Button(self.fm1, text="5", fg="red", width=10)
        # self.quit.grid(column=1, row=2)
        # self.quit = tk.Button(self.fm1, text="6", fg="red", width=10)
        # self.quit.grid(column=2, row=2)
        # self.quit = tk.Button(self.fm1, text="-", fg="red", width=10)
        # self.quit.grid(column=3, row=2)
        #
        # self.quit = tk.Button(self.fm1, text="7", fg="red", width=10)
        # self.quit.grid(column=0, row=3)
        # self.quit = tk.Button(self.fm1, text="8", fg="red", width=10)
        # self.quit.grid(column=1, row=3)
        # self.quit = tk.Button(self.fm1, text="9", fg="red", width=10)
        # self.quit.grid(column=2, row=3)
        # self.quit = tk.Button(self.fm1, text="+", fg="red", width=10)
        # self.quit.grid(column=3, row=3)
        #
        # self.quit = tk.Button(self.fm1, text="0", fg="red", width=10)
        # self.quit.grid(column=1, row=4)
        # self.quit = tk.Button(self.fm1, text=".", fg="red", width=10)
        # self.quit.grid(column=2, row=4)
        # self.quit = tk.Button(self.fm1, text="=", fg="red", width=10, command = self.ff)
        # self.quit.grid(column=3, row=4)
        self.ff()

    def create_widgets(self, index, chars):
        self.log.configure(state='normal')
        self.log.insert(index, chars)
        self.log.see('end')
        self.log.update()
        self.log.configure(state='disabled')

    def ff(self):
        for self.x in self.value:
            self.quit = tk.Button(self.fm1, text=self.x, fg="red", width=10, command=lambda x=self.x)
            self.quit.grid(column=0, row=self.x)



root = tk.Tk()
app = Application(master=root)
app.create_widgets("insert", "1、通过解压软件解压下载的.exe文件。\n")
app.create_widgets("end", "2、xxxxxxxxxxxxxxxxxxxx。\n")
app.mainloop()