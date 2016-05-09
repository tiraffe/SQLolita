# coding=utf-8
# Created by Tian Yuanhao on 2016/4/17.
import traceback

import time

from file_handler.data_dict import DataDict
from file_handler.table_file import TableFile
from index_handler.index_dict import IndexDict
from file_handler.user_dict import UserDict
from frontend.nodes import NodeType
from config.config import *
import query
import os

data_dict = DataDict(DATA_DICT_PATH)
index_dict = IndexDict(INDEX_PATH)
user_dict = UserDict(USER_PATH)


def execute_create_table(node):
    if data_dict.has_table(node.table_name):
        print "Error: This table already exists."
        return
    else:
        data_dict.dict[node.table_name] = node.attr_list
        data_dict.write_back()


def execute_show_tables(node):
    print data_dict.tables_name()


def execute_insert(node):
    if not data_dict.has_table(node.table_name):
        print "Error: The table does not exist."
        return
    table = TableFile(data_dict, node.table_name, node.value_list)
    if not table.insert(index_dict):
        print "Error: Types are not matched or index duplicated"
    index_dict.load_index()


def execute_drop_table(node):
    if not data_dict.has_table(node.table_name):
        print "Error: The table does not exist."
        return
    del data_dict.dict[node.table_name]     # remove data dict
    data_dict.write_back()
    os.remove(TABLES_PATH + node.table_name) # remove table file
    index_dict.drop_table(node.table_name)
    print "Drop table '%s' successful." % node.table_name


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
    for i in range(n): table += "─" * width + ("┴" if i != n - 1 else "┘")
    print table.decode('utf-8')


def execute_print_table(node):
    if not data_dict.has_table(node.table_name):
        print "Error: The table does not exist."
        return
    names = data_dict.table_attr_names(node.table_name)
    data = TableFile(data_dict, node.table_name).load_data()
    print_table(names, data)


def execute_alert(node):
    if not data_dict.has_table(node.table_name):
        print "Error: The table does not exist."
        return
    names = data_dict.table_attr_names(node.table_name)
    table = TableFile(data_dict, node.table_name)
    data = table.load_data()
    if node.op == "ADD":
        if node.attr_list.attr_name in names:
            print "Error: The attr's name already exists."
            return
        data_dict.dict[node.table_name] += [node.attr_list]
        for idx in range(len(data)): data[idx].append("NULL")
    elif node.op == "DROP":
        attr_name = node.attr_list[0]
        if attr_name not in names:
            print "Error: The attr's name does not exist."
            return
        old_list = data_dict.dict[node.table_name]
        data_dict.dict[node.table_name] = [attr for attr in old_list if attr.attr_name != attr_name]
        idx_remove = names.index(attr_name)
        for idx in range(len(data)): del data[idx][idx_remove]
        index_dict.drop_index(node.table_name, attr_name)
    table.data_list = data
    table.write_back()
    data_dict.write_back()
    print "Alert table successful."


def execute_delete(node):
    if not data_dict.has_table(node.table_name):
        print "Error: The table does not exist."
        return
    names = data_dict.table_attr_names(node.table_name)
    table = TableFile(data_dict, node.table_name)
    data = table.load_data()
    old_len = len(data)
    try:
        table.data_list = [line for line in data if not check_where(node.where_list, names, line)]
    except Exception, e:
        print "Error: %s." % e
        # print traceback.format_exc()
        return
    new_len = len(table.data_list)
    table.write_back()
    index_dict.load_index()
    print "%d line(s) are deleted." % (old_len - new_len)


def set_value(data, names, set_list):
    # print "set_value() data:" + str(data)
    dict = {}
    for idx in range(len(names)): dict[names[idx]] = data[idx]
    left = set_list[0].attr_name
    a = __get_value(set_list[0], dict)
    b = __get_value(set_list[1], dict)

    if a != 'NULL' and b != 'NULL' and type(a) != type(b):
        raise Exception("Type not match")
    data[names.index(left)] = b


def execute_update(node):
    if not data_dict.has_table(node.table_name):
        print "Error: The table does not exist."
        return
    names = data_dict.table_attr_names(node.table_name)
    table = TableFile(data_dict, node.table_name)
    data = table.load_data()
    updated_lines = 0
    try:
        for idx in range(len(data)):
            if check_where(node.where_list, names, data[idx]):
                updated_lines += 1
                set_value(data[idx], names, node.set_list)
    except Exception, e:
        print "Error: %s." % e
        # print traceback.format_exc()
        return
    table.write_back()
    print "%d line(s) are updated." % updated_lines


def __can_use_index(table_name, where_node, index_dict):
    if where_node.left.type == NodeType.relation_attr and where_node.right.type == NodeType.value \
            and where_node.op == "=" and index_dict.has_index(table_name, where_node.left.attr_name):
        return True
    else:
        return False


def dur( op=None, clock=[time.time()]):
    if op:
        duration = time.time() - clock[0]
        print '%s finished. Duration %.6f seconds.' % (op, duration)
    clock[0] = time.time()


def execute_select(node):
    dur()
    for table_name in node.from_list:
        if not data_dict.has_table(table_name):
            print "Error: The table '%s' does not exist." % table_name
            return
    part_name = []
    full_name = []
    table_data = []
    for table_name in node.from_list:
        names = data_dict.table_attr_names(table_name)
        part_name += names
        full_name += [table_name + '.' + attr_name for attr_name in names]
        table_data += [TableFile(data_dict, table_name).load_data()]

    name_dict = {}
    for idx in range(len(full_name)):
        name_dict[full_name[idx]] = idx
        name_dict[part_name[idx]] = idx

    if node.select_list[0] == "*":
        node.select_list = full_name
    try:
        select_col_nums = [name_dict[str(attr_name)] for attr_name in node.select_list]
        res = query.joint(table_data)
        if len(node.from_list) == 1 and __can_use_index(node.from_list[0], node.where_list, index_dict):
            val = node.where_list.right.value
            num = index_dict.query(node.from_list[0], node.where_list.left.attr_name, [val])[0]
            res = [res[num]]
        else:
            res = [line for line in res if check_where(node.where_list, part_name, line, full_name)]
        res = query.projection(res, select_col_nums)
        print_table(node.select_list, res)
        dur("Select")
    except Exception, e:
        print "Error: %s." % e
        print traceback.format_exc()


def execute_create_index(node):
    if not data_dict.has_table(node.table_name):
        print "Error: The table does not exist."
        return
    attr_names = data_dict.table_attr_names(node.table_name)
    if node.attr_name not in attr_names:
        print "Error: The table_attr does not exist."
        return
    if index_dict.has_index(node.table_name, node.attr_name):
        print "Error: The index already exist."
        return
    data = TableFile(data_dict, node.table_name).load_data()
    index_dict.create_index(node.table_name, node.attr_name, attr_names, data)
    index_dict.write_back()


def execute_drop_index(node):
    if not data_dict.has_table(node.table_name):
        print "Error: The table does not exist."
        return
    attr_names = data_dict.table_attr_names(node.table_name)
    if node.attr_name not in attr_names:
        print "Error: The table_attr does not exist."
        return
    if not index_dict.has_index(node.table_name, node.attr_name):
        print "Error: The index does not exist."
        return
    index_dict.drop_index(node.table_name, node.attr_name)


def __get_value(node, dict):
    if node.type == NodeType.relation_attr:
        return dict[str(node)]
    else:
        return node.value


def __check_node(node, dict):
    assert(node.type == NodeType.condition)
    if node.op == "AND":
        return __check_node(node.left, dict) and __check_node(node.right, dict)
    elif node.op == "OR":
        return __check_node(node.left, dict) or __check_node(node.right, dict)
    elif node.op == ">=":
        return __get_value(node.left, dict) >= __get_value(node.right, dict)
    elif node.op == "<=":
        return __get_value(node.left, dict) <= __get_value(node.right, dict)
    elif node.op == ">":
        return __get_value(node.left, dict) > __get_value(node.right, dict)
    elif node.op == "<":
        return __get_value(node.left, dict) < __get_value(node.right, dict)
    elif node.op == "=":
        return __get_value(node.left, dict) == __get_value(node.right, dict)
    elif node.op == "!=":
        return __get_value(node.left, dict) != __get_value(node.right, dict)


def check_where(where_node, part_names, data_line, full_names = None):
    assert len(part_names) == len(data_line)
    if not where_node: return True
    dict = {}
    for idx in range(len(part_names)):
        dict[part_names[idx]] = data_line[idx]
    if full_names:
        for idx in range(len(full_names)):
            dict[full_names[idx]] = data_line[idx]
    return __check_node(where_node, dict)


def execute_create_user(node):
    if node.user_id in user_dict.password.keys():
        print "Error: The username already existed."
    user_dict.create_user(node.user_id, node.password)
    user_dict.write_back()


def execute_main(command):
    if command.type == NodeType.create_table:
        execute_create_table(command)
    elif command.type == NodeType.show_tables:
        execute_show_tables(command)
    elif command.type == NodeType.drop_table:
        execute_drop_table(command)
    elif command.type == NodeType.insert:
        execute_insert(command)
    elif command.type == NodeType.alert:
        execute_alert(command)
    elif command.type == NodeType.delete:
        execute_delete(command)
    elif command.type == NodeType.update:
        execute_update(command)
    elif command.type == NodeType.select:
        execute_select(command)
    elif command.type == NodeType.print_table:
        execute_print_table(command)
    elif command.type == NodeType.create_index:
        execute_create_index(command)
    elif command.type == NodeType.drop_index:
        execute_drop_index(command)
    elif command.type == NodeType.create_user:
        execute_create_user(command)
