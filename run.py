# coding=utf-8
# Created by Tian Yuanhao on 2016/4/17.
import getpass

from frontend.lexer import lexer as lex
from frontend.parser import parser
from execute.main import execute_main
from config.config import LOGIN_PASSWORD

def login():
    password = getpass.getpass('Enter password: ')
    return password == LOGIN_PASSWORD

while not login():
    print "Password is not correct!"

while True:
    command = raw_input("SQLolita > ")
    while ';' not in command:
        command += " " + raw_input()

    result = parser.parse(command, lexer=lex)
    if not result: continue
    if result.type == "EXIT": break

    # print "OK"
    execute_main(result)