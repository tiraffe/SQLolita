# coding=utf-8
# Created by Tian Yuanhao on 2016/4/5.


class QueryNode():
    def __init__(self, select_list, from_list, where_list):
        self.type = 'SELECT'
        self.select_list = select_list
        self.from_list = from_list
        self.where_list = where_list


class InsertNode():
    def __init__(self, table_name, value_list):
        self.type = 'INSERT'
        self.table_name = table_name
        self.value_list = value_list


class DeleteNode():
    def __init__(self, table_name, where_list):
        self.type = 'DELETE'
        self.table_name = table_name
        self.where_list = where_list


class UpdateNode():
    def __init__(self, table_name, set_list, where_list):
        self.type = 'UPDATE'
        self.table_name = table_name
        self.where_list = where_list


class AlertNode():
    def __init__(self, table_name, op, attr_list):
        self.type = 'ALERT'
        self.table_name = table_name
        self.op = op
        self.rel_list = attr_list


class CreateTableNode():
    def __init__(self, table_name, attr_list):
        self.type = 'CREATETABLE'
        self.table_name = table_name
        self.attr_list = attr_list


class DropTableNode():
    def __init__(self, table_name):
        self.type = 'DROPTABLE'
        self.table_name = table_name


class CreateIndexNode():
    def __init__(self, table_name, attr_name):
        self.type = 'CREATEINDEX'
        self.table_name = table_name
        self.attr_name = attr_name


class DropIndexNode():
    def __init__(self, table_name, attr_name):
        self.type = 'DROPTABLE'
        self.table_name = table_name
        self.attr_name = attr_name


class CreateUserNode():
    def __init__(self, user_id, password):
        self.type = 'CREATEUSER'
        self.user_id = user_id
        self.password = password


class GrantUserNode():
    def __init__(self):
        pass


class RevokeUserNode():
    def __init__(self):
        pass


class PrintTable():
    def __init__(self, table_name):
        self.type = 'PRINT'
        self.table_name = table_name


class ShowTables():
    def __init__(self, table_name):
        self.type = 'SHOWTABLES'
        self.table_name = table_name


