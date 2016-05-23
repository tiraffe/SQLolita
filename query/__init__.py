# coding=utf-8
# Created by Tian Yuanhao on 2016/4/18.


def projection(table, col_num_list):
    res = []
    for line in table:
        new_line = [line[i] for i in col_num_list]
        res += [new_line]
    return res


def joint(tables):
    res = None
    for table in tables:
        if res is None:
            res = table
            continue
        temp = []
        for x in res:
            for y in table:
                temp += [x + y]
        res = temp
    return res


def select(table, col_num_list):
    return [table[i] for i in col_num_list]


def joint_by_index(tables, table_name, index_name, index_dict):
    res = []
    for line in tables[1]:
        x = line[0]
        num = index_dict.query(table_name, index_name, [x])[0]
        if num is not None:
            res += [tables[0][num] + line]
    return res

def can_use_index(where_list, index_dict):
    return False