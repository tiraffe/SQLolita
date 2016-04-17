# coding=utf-8
# Created by Tian Yuanhao on 2016/4/17.
from frontend.lexer import lexer as lex
from frontend.parser import parser
from main.execute import execute_main

while True:
    line = raw_input("SQLolita >")
    while ';' not in line:
        line += ' ' + raw_input()

    result = parser.parse(line, lexer=lex)
    if not result: continue

    # print "OK"
    execute_main(result)
