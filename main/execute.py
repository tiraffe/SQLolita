# coding=utf-8
# Created by Tian Yuanhao on 2016/4/17.
from frontend.nodes import NodeType


def execute_main(command):
    type = command.type
    if type == NodeType.create_table:
        print "create table"
    elif type == NodeType.show_tables:
        pass
    elif type == NodeType.drop_table:
        pass
    elif type == NodeType.insert:
        pass
    elif type == NodeType.alert:
        pass
    elif type == NodeType.delete:
        pass
    elif type == NodeType.update:
        pass
    elif type == NodeType.select:
        pass
    elif type == NodeType.print_table:
        pass
    elif type == NodeType.create_table:
        pass
