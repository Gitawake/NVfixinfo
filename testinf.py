#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import threading


class LogicScript:

    def __init__(self):
        self.path = ''
        self.discoloration = None
        self.inf_path = R'/Display.Driver/nvcvi.inf'
        self.a_value = R'PCI\VEN_10DE&DEV_1C60&SUBSYS_6A031558'
        self.b_value = R'PCI\VEN_10DE&DEV_1C60&SUBSYS_74811558'

    def file_path(self):
        if not self.path:
            return
        self.discoloration = threading.Thread(target=self.modification)
        self.discoloration.start()

    def modification(self):
        if not os.path.exists(self.path + '/setup.exe'):
            return
        if not os.path.exists(self.path + self.inf_path):
            return
        infox = open(self.path + self.inf_path, mode='tr')
        data = infox.read()
        finds = data.find(self.a_value)
        if finds == -1:
            return
        data = data.replace(self.a_value, self.b_value)
        conserve = open(self.path + self.inf_path, mode='w', encoding='utf-8')
        conserve.write(data)
        conserve.close()
        start = input('是否启动安装程序？ Y/N:')
        if start == 'Y' or start == 'y':
            return
        self.installing_the_drive()

    def installing_the_drive(self):
        if os.system('bcdedit.exe /set nointegritychecks on') != 0:
            return
        os.system(self.path + '/setup.exe')
        if os.system('bcdedit.exe /set nointegritychecks off') != 0:
            return


if __name__ == '__main__':
    ls = LogicScript()
    ls.file_path()
