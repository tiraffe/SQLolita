# coding=utf-8
# Created by Tian Yuanhao on 2016/4/17.
from frontend.lexer import lexer as lex
from frontend.parser import parser
from execute.main import execute_main


while True:
    command = raw_input("SQLolita > ")
    while ';' not in command:
        command += " " + raw_input()

    result = parser.parse(command, lexer=lex)
    if not result: continue
    if result.type == "EXIT": break

    # print "OK"
    execute_main(result)
