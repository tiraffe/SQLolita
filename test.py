# coding=utf-8
# Created by Tian Yuanhao on 2016/4/5.
from string import upper

from frontend.lexer import lexer as lex
from frontend.parser import parser

create_table_test = """
create table A (
  id int,
  name char(10),
  age int,
  grade int,
);
"""

insert_test = "insert into A values('x', 1, 2, 3), ('y', 3, 4, 5);"

delete_test = "delete from A where id = 1;"

update_test = "update A set age = 1 where id = 2;"

print_test = "print A;"

alert_add_test = "alert table A add num char(20);"

alert_drop_test = "alert table A drop num;"

drop_table_test = "drop table mumu;"


def exec_sql(sql):
    res = parser.parse(sql, lexer=lex)
    from execute.main import execute_main
    execute_main(res)

def f(x):
    x += 1

a = 1
f(a)
print a
# exec_sql("print A;")
# exec_sql("print G;")
# exec_sql("select G.id, A.id from G, A where G.id > 2 and G.id > A.id;")
