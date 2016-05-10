# coding=utf-8
# Created by Tian Yuanhao on 2016/4/17.
import getpass

from frontend.lexer import lexer as lex
from frontend.parser import parser
from execute.main import execute_main
from config.config import *
from handler.user_dict import UserDict

user_dict = UserDict(USER_PATH)


def login():
    username = raw_input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    if user_dict.check(username, password):
        UserDict.CurrentUser = username
        user_dict.show_power(username)
        return True
    else:
        return False

if __name__ == "__main__":

    # while not login(): print "Password or username is not correct!"

    while True:
        command = raw_input("SQLolita > ")
        while ';' not in command:
            command += " " + raw_input()

        result = parser.parse(command, lexer=lex)
        if not result: continue
        if result.type == "EXIT": break

        # print "OK"
        execute_main(result)
