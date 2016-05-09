# coding=utf-8
# Created by Tian Yuanhao on 2016/5/6.

from b_plus_tree import BPTree
from file_handler.data_dict import DataDict
from file_handler.table_file import TableFile
from config.config import *


class IndexDict:
    def __init__(self, file_path):
        self.file_path = file_path
        self.index_dict = {}
        self.load_index()

    def has_index(self, table_name, attr_name):
        return table_name in self.index_dict.keys() and attr_name in self.index_dict[table_name].keys()

    def drop_index(self, table_name, attr_name):
        del self.index_dict[table_name][attr_name]
        if len(self.index_dict[table_name]) == 0:
            del self.index_dict[table_name]
        self.write_back()

    def drop_table(self, table_name):
        if table_name in self.index_dict.keys():
            del self.index_dict[table_name]
        self.write_back()

    def create_index(self, table_name, attr_name, attr_names, table_data):
        if table_name not in self.index_dict:
            self.index_dict[table_name] = {}
        self.index_dict[table_name][attr_name] = IndexHandler(attr_name, attr_names)
        self.index_dict[table_name][attr_name].create_index(table_data)
        self.__log_tree(table_name, attr_name)

    def load_index(self):
        self.index_dict = {}
        data_dict = DataDict(DATA_DICT_PATH)
        f = open(self.file_path, "r")
        attr_names = None
        table_name = None
        table_data = None
        for line in f.readlines():
            items = line.split()
            if len(items) < 1: continue

            if items[0][0] == '[':
                table_name = items[0][1:-1]
                attr_names = data_dict.table_attr_names(table_name)
                table_data = TableFile(data_dict, table_name).load_data()
            else:
                self.create_index(table_name, items[0], attr_names, table_data)

    def write_back(self):
        f = open(self.file_path, "w")
        for (table_name, table) in self.index_dict.items():
            f.write('[' + table_name + ']\n')
            for (index_name, index) in table.items():
                f.write(str(index_name) + '\n')
        f.close()

    # return lines number.
    def query(self, table_name, attr_name, key_list):
        return self.index_dict[table_name][attr_name].query_by_index(key_list)

    def __log_tree(self, table_name, attr_name):
        path  = "database/index/"
        f = open(path + table_name + "_" + attr_name, 'w')
        f.write(str(self.index_dict[table_name][attr_name].tree))


class IndexHandler:
    def __init__(self, index_attr, attr_names):
        self.index_attr = index_attr
        self.attr_names = attr_names
        self.pos = self.attr_names.index(self.index_attr)
        self.tree = BPTree(BP_TREE_SIZE)

    # Insert data into BP_tree.
    def create_index(self, data):
        self.tree.clear()
        nl = 0
        for line in data:
            self.tree.insert(line[self.pos], nl)
            nl += 1

    def has(self, key):
        return self.tree.exist(key)

    def query_by_index(self, keys):
        res = []
        for key in keys:
            res += [self.tree.get(key)]
        return res


if __name__ == '__main__':
    pass