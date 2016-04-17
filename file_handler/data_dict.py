# coding=utf-8
# Created by Tian Yuanhao on 2016/4/12.
from frontend.nodes import AttrType


class DataDict:
    def __init__(self, file_path):
        self.dict = {}
        self.file_path = file_path
        self.load_data()

    def tables_name(self):
        return self.dict.keys()

    def load_data(self):
        f = open(self.file_path, "r")
        table_name = "default"
        while True:
            line = f.readline()
            if not line: break
            if len(line) == "\n": continue

            if line[0] == '[':
                table_name = line[1:-2]
                print table_name
            elif len(line) > 1:
                items = line[:-1].split()
                if not self.dict.has_key(table_name):
                    self.dict[table_name] = [AttrType(*items)]
                else:
                    self.dict[table_name] += [AttrType(*items)]
        f.close()

    def write_back(self):
        text = ""
        for key, val in self.dict.items():
            text += "[" + key + "]\n"
            for type in val: text += str(type) + "\n"
            text += "\n"
        f = open(self.file_path, "w")
        f.write(text)
        f.close()



data = DataDict("data.txt")
print data.tables_name()

# data.dict = {
#     "A" : [AttrType("age", "INT", 0), AttrType("name", "CHAR", 10)],
#     "B" : [AttrType("age", "INT", 0), AttrType("name", "CHAR", 10), AttrType("age", "PK", 0)]
# }
# data.write_back()

