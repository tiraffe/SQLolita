# coding=utf-8
# Created by Tian Yuanhao on 2016/4/26.


class LeafNode :
    def __init__(self, keys, values):
        self.type = "leaf"
        self.keys = keys
        self.values = values
        self.next_page = None
        self.parent = None


class InteriorNode:
    def __init__(self, keys, pointers):
        self.type = "interior"
        self.keys = keys
        self.pointers = pointers
        self.parent = None


class BPTree:
    def __init__(self, node_size):
        left, right = LeafNode([], []), LeafNode([], [])
        self.root = InteriorNode([0], [left, right])
        left.parent = right.parent = self.root
        left.next_page = right
        self.node_size = node_size

    # In an increasing list, find first i that key < list[i].
    @staticmethod
    def __find_position(key, list):
        n = len(list)
        for i in range(n):
            if key < list[i]:
                return i
        return n

    def __left_brother(self, node):
        parent = node.parent
        pos = self.__find_position(node.keys[0], parent.keys)
        return parent.pointers[pos - 1] if pos != 0 else None

    def __right_brother(self, node):
        parent = node.parent
        pos = self.__find_position(node.keys[0], parent.keys)
        return parent.pointers[pos + 1] if pos + 1 < len(parent.pointers) else None

    # Search the leaf.
    def search(self, key):
        return self.__search(key, self.root)

    def __search(self, key, node):
        if node.type == 'left':
            return node
        else:
            pos = self.__find_position(key, node.keys)
            return self.__search(key, node.pointers[pos])

    # Insert a new pair(key, val).
    def insert(self, key, val):
        leaf = self.search(key)
        self.__insert(leaf, key, val)

    def __insert(self, node, key, val):
        if self.node_size > len(node.keys):
            self.__insert_into_leaf(node, key, val)
        elif self.node_size > len(node.parent.keys):
            self.__insert_into_leaf(node, key, val)
            (left, mid_val, right) = self.__split_leaf(node)
            self.__insert_into_interior(node.parent, left, mid_val, right)

    def __insert_into_leaf(self, node, key, val):
        pos = self.__find_position(key, node.keys)
        node.keys.insert(pos, key)
        node.values.insert(pos, val)

    def __insert_into_interior(self, node, left_node, mid_key, right_node):
        if node is None:
            self.root = InteriorNode(keys=[mid_key], pointers=[left_node, right_node])
            left_node.parent = right_node.parent = self.root
            self.root.parent = None
        else:
            pos = self.__find_position(mid_key, node.keys)
            node.keys.insert(pos, mid_key)
            node.pointers[pos] = left_node
            node.pointers.insert(pos + 1, right_node)
            if len(node.keys) > self.node_size:
                left, mid_val, right = self.__split_interior(node)
                self.__insert_into_interior(node.parent, left, mid_val, right)

    def __split_leaf(self, node):
        mid_pos = self.node_size / 2
        left_keys = [node.keys[i] for i in range(mid_pos)]
        left_values = [node.values[i] for i in range(mid_pos)]
        left = LeafNode(left_keys, left_values)
        right_keys = [node.keys[i] for i in range(mid_pos, self.node_size + 1)]
        right_values = [node.values[i] for i in range(mid_pos, self.node_size + 1)]
        right = LeafNode(right_keys, right_values)
        left.next_page = right
        return left, node.values[mid_pos], right

    def __split_interior(self, node):
        mid_pos = self.node_size / 2
        left_keys = [node.keys[i] for i in range(mid_pos)]
        left_pointers = [node.pointers[i] for i in range(mid_pos)]
        left = InteriorNode(left_keys, left_pointers)
        right_keys = [node.keys[i] for i in range(mid_pos, self.node_size + 1)]
        right_pointers = [node.pointers[i] for i in range(mid_pos, self.node_size + 1)]
        right = InteriorNode(right_keys, right_pointers)
        return left, node.values[mid_pos], right

    def delete(self, key):
        leaf = self.search(key)
        self.__delete(self.root, key)

    def __delete(self, node, key):
        # TODO delete
        pass

