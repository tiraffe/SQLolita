# coding=utf-8
# Created by Tian Yuanhao on 2016/5/8.
from config.config import USER_PATH


class UserDict:
    CurrentUser = "admin"

    def __init__(self, path):
        self.password = {}
        self.disable = {}
        self.path = path
        self.load_data()

    def check(self, user_name, password):
        return (user_name, password) in self.password.items()

    def create_user(self, name, password):
        self.password[name] = password

    def load_data(self):
        f = open(self.path, 'r')
        for line in f.readlines():
            items = line.split()
            if items[0] == '#':
                self.password[items[1]] = items[2]
            elif items[0] == '!':
                pass
        f.close()
        if len(self.password) == 0:
            self.password['admin'] = 'admin'

    def write_back(self):
        f = open(self.path, "w")
        for key, val in self.password.items():
            f.write(key + " " + val + "\n")
        f.close()
