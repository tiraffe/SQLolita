# coding=utf-8
# Created by Tian Yuanhao on 2016/5/8.
from config.config import USER_PATH
from frontend.nodes import NodeType


class UserDict:
    CurrentUser = "admin"
    ALL_POWER = [NodeType.select, NodeType.update, NodeType.delete, NodeType.insert, NodeType.create_table,
                 NodeType.drop_table, NodeType.drop_index, NodeType.create_index, NodeType.alert,
                 NodeType.create_user, NodeType.print_table]
    DEFAULT_POWER = [NodeType.select, NodeType.print_table]

    def __init__(self, path=USER_PATH):
        self.password = {}  # username, password
        self.power = {}     # username, {table_name, power_mask}
        self.path = path
        self.load_data()

    def check(self, user_name, password):
        return (user_name, password) in self.password.items()

    def create_table(self, table_name):
        for username, power_dict in self.power.items():
            if username != "admin":
                self.add_power([username], [table_name], self.DEFAULT_POWER)
        self.write_back()

    def drop_table(self, table_name):
        for username, power_dict in self.power.items():
            if username == "admin": continue
            del self.power[username][table_name]
        self.write_back()

    def has_power(self, table_list, power_list, user_name=None):
        if not user_name:
            user_name = self.CurrentUser
        for table_name in table_list:
            for power_type in power_list:
                if not self.__has_power(user_name, table_name, power_type):
                    return False
        return True

    def __has_power(self, user_name, table_name, power_type):
        if user_name == 'admin':
            return True
        else:
            assert user_name in self.power
            if table_name not in self.power[user_name]:
                return False
            pos = self.ALL_POWER.index(power_type)
            mask = self.power[user_name][table_name]
            return (mask & (1 << pos)) != 0

    def create_user(self, username, password, table_names):
        self.password[username] = password
        self.power[username] = {}
        for table_name in table_names:
            self.power[username][table_name] = self.__get_mask(self.DEFAULT_POWER)

    def add_power(self, user_list, table_list, power_list):
        for user_name in user_list:
            for table_name in table_list:
                self.__add_power(user_name, table_name, power_list)

    def __add_power(self, user_name, table_name, power_list):
        if not user_name in self.power:
            self.power[user_name] = {}
        if table_name in self.power[user_name]:
            self.power[user_name][table_name] |= self.__get_mask(power_list)
        else:
            self.power[user_name][table_name] = self.__get_mask(power_list)

    def remove_power(self, user_list, table_list, power_list):
        for user_name in user_list:
            for table_name in table_list:
                self.__remove_power(user_name, table_name, power_list)

    def __remove_power(self, user_name, table_name, power_list):
        assert user_name in self.power and table_name in self.power[user_name]
        self.power[user_name][table_name] &= ~self.__get_mask(power_list)

    def show_power(self, user_name):
        print "Power List:"
        print "Username: " + user_name
        for table_name, mask in self.power[user_name].items():
            power_list = []
            for pos in range(len(self.ALL_POWER)):
                if (mask & (1 << pos)) != 0:
                    power_list.append(self.ALL_POWER[pos])
            print "Table %s: %s." % (table_name, str(power_list))

    def __get_power(self, power_mask):
        power_list = []
        for pos in range(len(self.ALL_POWER)):
            if (power_mask & (1 << pos)) != 0:
                power_list.append(self.ALL_POWER[pos])
        return power_list

    def __get_mask(self, power_list):
        res = 0
        for power_type in power_list:
            assert power_type in self.ALL_POWER
            pos = self.ALL_POWER.index(power_type)
            res |= 1 << pos
        return res

    def load_data(self):
        f = open(self.path, 'r')
        username = None
        for line in f.readlines():
            items = line.split()
            if len(items) < 2: continue
            if items[0] == '#':
                username = items[1]
                self.password[username] = items[2]
            elif items[0] == '$':
                self.add_power([username], [items[1]], items[2:])
        f.close()
        if len(self.password) == 0:
            self.password['admin'] = 'admin'
            self.power['admin'] = {'ALL' : -1}

    def write_back(self):
        f = open(self.path, "w")
        for username in self.password.keys():
            f.write("# " + username + " " + self.password[username] + "\n")
            for table_name, mask in self.power[username].items():
                f.write("$ " + table_name + " ")
                for power in self.__get_power(mask): f.write(power + " ")
                f.write("\n")
        f.close()
