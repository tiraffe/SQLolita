# coding=utf-8
# Created by Tian Yuanhao on 2016/4/17.
from file_handler.data_dict import DataDict
from file_handler.table_file import TableFile
from frontend.nodes import NodeType
from config.config import *
import os


def execute_create_table(node):
    data_dict = DataDict(DATA_DICT_PATH)
    if data_dict.has_table(node.table_name):
        print "Error: This table already exists."
        return
    else:
        data_dict.dict[node.table_name] = node.attr_list
        data_dict.write_back()


def execute_show_tables(node):
    data_dict = DataDict(DATA_DICT_PATH)
    print data_dict.tables_name()


def execute_insert(node):
    data_dict = DataDict(DATA_DICT_PATH)
    if not data_dict.has_table(node.table_name):
        print "Error: The table does not exist."
        return
    table = TableFile(data_dict, node.table_name, node.value_list)
    table.insert()


def execute_drop_table(node):
    data_dict = DataDict(DATA_DICT_PATH)
    if not data_dict.has_table(node.table_name):
        print "Error: The table does not exist."
        return
    del data_dict.dict[node.table_name]     # remove data dict
    data_dict.write_back()
    os.remove(TABLES_PATH + node.table_name) # remove table file
    # TODO remove index


def print_table(names, data, width = COLUMN_WIDTH):
    table = "┌"
    n = len(names)
    for i in range(n): table += "─" * width + ("┬" if i != n - 1 else "┐\n")
    fmt = "│%" + str(width*2) + "s"
    for name in names: table += fmt % name
    table += "│\n├"
    for i in range(n): table += "─" * width + ("┼" if i != n - 1 else "┤\n")
    for line in data:
        for item in line: table += fmt % item
        table += "│\n"
    table += "└"
    for i in range(n): table += "─" * width + ("┴" if i != n - 1 else "┘\n")
    print table


def execute_print_table(node):
    data_dict = DataDict(DATA_DICT_PATH)
    if not data_dict.has_table(node.table_name):
        print "Error: The table does not exist."
        return
    names = data_dict.table_attr_names(node.table_name)
    data = TableFile(data_dict, node.table_name).load_data()
    print_table(names, data)

def execute_main(command):
    """
    执行相应sql命令
    :param command: sql语法树根节点
    :return:
    """
    type = command.type
    if type == NodeType.create_table:
        execute_create_table(command)
    elif type == NodeType.show_tables:
        execute_show_tables(command)
    elif type == NodeType.drop_table:
        execute_drop_table(command)
    elif type == NodeType.insert:
        execute_insert(command)
    elif type == NodeType.alert:
        pass
    elif type == NodeType.delete:
        pass
    elif type == NodeType.update:
        pass
    elif type == NodeType.select:
        pass
    elif type == NodeType.print_table:
        execute_print_table(command)

