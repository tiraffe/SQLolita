# coding=utf-8
# Created by Tian Yuanhao on 2016/4/17.
from config.config import TABLES_PATH


class TableFile:
    def __init__(self, data_dict, table_name, insert_list = None):
        self.attrs = [attr for attr in data_dict.dict[table_name] if attr.attr_type != "PK"]
        self.PK = [attr.attr_name for attr in data_dict.dict[table_name] if attr.attr_type == "PK"]
        self.table_name = table_name
        self.insert_list = insert_list or []
        self.data_list = []

    def load_data(self):
        f = open(TABLES_PATH + self.table_name, 'a+')
        while True:
            line = f.readline()
            if not line: break
            items = line[:-1].split()
            self.data_list.append(items)
        f.close()
        return self.data_list

    def write_back(self):
        f = open(TABLES_PATH + self.table_name, 'w')
        for line in self.data_list:
            for word in line: f.write(str(word) + " ")
            f.write("\n")
        f.close()

    def insert(self):
        f = open(TABLES_PATH + self.table_name, 'a')
        if not self.__check_type() or not self.__check_index():
            return False
        text = ""
        for value_list in self.insert_list:
            for value in value_list: text += str(value.value) + " "
            text += '\n'
        f.write(text)
        f.close()

    def __check_index(self):
        # TODO check index.
        return True

    def __check_type(self):
        for val_list in self.insert_list:
            if len(val_list) != len(self.attrs):
                print "Error: Lengths are not matched."
                return False

            for idx in range(len(val_list)):
                if not TableFile.__is_type_match(val_list[idx], self.attrs[idx]):
                    print "Error: Type and value are not matched."
                    return False
        return True

    @staticmethod
    def __is_type_match(val, attr):
        if val.value_type == "NUMBER" and attr.attr_type == "INT":
            return True
        elif val.value_type == "STRING" and attr.attr_type == "CHAR" and len(val.value) <= attr.type_len:
            return True
        elif val.value_type == "NULL":
            return True
        else:
            return False


if __name__ == "__main__":
    from data_dict import DataDict
    data = DataDict("../database/dict.txt")
    table = TableFile(data, 'A')
    table.load_data()
    table.write_back()