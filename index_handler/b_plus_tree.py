# coding=utf-8
# Created by Tian Yuanhao on 2016/4/26.
import random


class LeafNode :
    def __init__(self, keys, values):
        self.type = "leaf"
        self.keys = keys
        self.values = values
        self.parent = None

    def __str__(self):
        return '(key: ' + str(self.keys) + ', val: '+ str(self.values) + ')'


class InteriorNode:
    def __init__(self, keys, pointers):
        self.type = "interior"
        self.keys = keys
        self.pointers = pointers
        self.parent = None

    def __str__(self):
        res =  '[key: ' + str(self.keys)  + ', \npointers:\n'
        for ptr in self.pointers:
            res += str(ptr) + '\n'
        return res + ']'


class BPTree:
    def __init__(self, node_size):
        self.root = LeafNode([], [])
        self.node_size = node_size
        self.total = 0

    def __str__(self):
        return str(self.root)

    def count_values(self):
        return  self.__count_values(self.root, None)

    def exist(self, key):
        node = self.search(key)
        return node and key in node.keys

    def __count_values(self, node, parent):
        if parent:
            assert node.parent == parent
        res = 0
        if node.type == 'leaf':
            return len(node.values)
        else:
            for u in node.pointers:
               res += self.__count_values(u, node)
        return res

    # In an increasing list, find first i that key < list[i].
    @staticmethod
    def __find_position(key, list):
        n = len(list)
        for i in range(n):
            if key < list[i]:
                return i
        return n

    def __left_sibling(self, node):
        if not node.parent:
            return None
        parent = node.parent
        pos = self.__find_position(node.keys[0], parent.keys)
        return parent.pointers[pos - 1] if pos != 0 else None

    def __right_sibling(self, node):
        if not node.parent:
            return None
        parent = node.parent
        pos = self.__find_position(node.keys[0], parent.keys)
        return parent.pointers[pos + 1] if pos + 1 < len(parent.pointers) else None

    # Search the leaf.
    def search(self, key):
        return self.__search(key, self.root)

    def __search(self, key, node):
        assert len(node.keys) <= self.node_size
        if node.type == 'leaf':
            return node
        else:
            pos = self.__find_position(key, node.keys)
            return self.__search(key, node.pointers[pos])

    # Insert a new pair(key, val).
    def insert(self, key, val):
        if self.exist(key):
            return False
        leaf = self.search(key)
        self.__insert(leaf, key, val)
        self.total += 1
        return True

    def __insert(self, node, key, val):
        if self.node_size > len(node.keys):
            self.__insert_into_leaf(node, key, val)
        else:
            self.__insert_into_leaf(node, key, val)
            (left, mid_key, right) = self.__split_leaf(node)
            self.__insert_into_interior(node.parent, left, mid_key, right)

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
        mid_pos = (self.node_size + 1) / 2
        left_keys = [node.keys[i] for i in range(mid_pos)]
        left_values = [node.values[i] for i in range(mid_pos)]
        left = LeafNode(left_keys, left_values)
        right_keys = [node.keys[i] for i in range(mid_pos, self.node_size + 1)]
        right_values = [node.values[i] for i in range(mid_pos, self.node_size + 1)]
        right = LeafNode(right_keys, right_values)
        left.parent = right.parent = node.parent
        return left, node.keys[mid_pos], right

    def __split_interior(self, node):
        mid_pos = (self.node_size + 1) / 2
        left_keys = [node.keys[i] for i in range(mid_pos)]
        left_pointers = [node.pointers[i] for i in range(mid_pos + 1)]
        left = InteriorNode(left_keys, left_pointers)
        right_keys = [node.keys[i] for i in range(mid_pos + 1, self.node_size + 1)]
        right_pointers = [node.pointers[i] for i in range(mid_pos + 1, self.node_size + 2)]
        right = InteriorNode(right_keys, right_pointers)
        left.parent = right.parent = node.parent
        for child in left.pointers: child.parent = left
        for child in right.pointers: child.parent = right
        return left, node.keys[mid_pos], right

    def delete(self, key):
        leaf = self.search(key)
        if key not in leaf.keys:
            return False
        else:
            self.__delete(leaf, key)
            self.total -= 1
            return True

    def __delete(self, node, key):
        pos = node.keys.index(key)
        del node.keys[pos]
        del node.values[pos]
        if len(node.keys) > self.node_size / 2:
            pass  # Already dene.
        else:
            left_sibling = self.__left_sibling(node)
            right_sibling = self.__right_sibling(node)
            if left_sibling and len(left_sibling.keys) > self.node_size / 2:
                move_key = left_sibling.keys.pop()
                move_val = left_sibling.values.pop()
                pos = self.__find_position(move_key, node.parent.keys)
                node.parent.keys[pos] = move_key  # TODO list assignment index out of range
                node.keys.insert(0, move_key)
                node.values.insert(0, move_val)
            elif right_sibling and len(right_sibling.keys) > self.node_size / 2:
                move_key = right_sibling.keys[0]
                move_val = right_sibling.values[0]
                del right_sibling.keys[0]
                del right_sibling.values[0]
                pos = self.__find_position(node.keys[-1], node.parent.keys)
                node.parent.keys[pos] = move_key  # TODO list assignment index out of range
                node.keys.append(move_key)
                node.values.append(move_val)
            elif left_sibling is not None:
                left_sibling.keys += [node.keys]
                left_sibling.values += [node.values]
                pos = self.__find_position(left_sibling.keys[0], node.parent.keys)
                self.__delete_interior_node(node.parent, pos)
            elif right_sibling is not None:
                node.keys += [right_sibling]
                node.values += [right_sibling]
                pos = self.__find_position(right_sibling.keys[0], node.parent.keys) - 1
                self.__delete_interior_node(node.parent, pos)

    def __delete_interior_node(self, node, pos):
        if node is None:
            return
        if node == self.root:
            if len(node.keys) == 1:
                self.root = self.root.pointers[0]
            else:
                del self.root.keys[pos]
                del self.root.pointers[pos + 1]
        else:
            left_sibling = self.__left_sibling(node)
            right_sibling = self.__right_sibling(node)
            del node.keys[pos]   # TODO list assignment index out of range
            del node.pointers[pos + 1]  # TODO list assignment index out of range
            if len(node.keys) > 0:
                pass # Already dene.
            else:
                if left_sibling and len(left_sibling.keys) > 1:
                    move_key = left_sibling.keys.pop()
                    move_ptr = left_sibling.pointers.pop()
                    pos = self.__find_position(move_key, node.parent.keys)
                    node.keys.insert(0, node.parent.keys[pos])
                    node.pointers.insert(0, move_ptr)
                    node.parent.keys[pos] = move_key
                elif right_sibling and len(right_sibling.keys) > 1:
                    move_key = right_sibling.keys[0]
                    move_ptr = right_sibling.pointers[0]
                    del right_sibling.keys[0]
                    del right_sibling.pointers[0]
                    pos = self.__find_position(move_key, node.parent.keys) - 1
                    node.keys.append(node.parent.keys[pos])
                    node.pointers.append(move_ptr)
                    node.parent.keys[pos] = move_key
                elif left_sibling is not None:
                    pos = self.__find_position(left_sibling.key[0], node.parent.keys)
                    left_sibling.keys.append(node.parent.keys[pos])
                    left_sibling.pointers.append(node.pointers[0])
                    self.__delete_interior_node(node.parent, pos)
                elif right_sibling is not None:
                    pos = self.__find_position(right_sibling.keys[0], node.parent.keys) - 1
                    right_sibling.keys.append(node.parent.keys[pos])
                    right_sibling.pointers.append(node.pointers[0])
                    self.__delete_interior_node(node.parent, pos)


if __name__ == "__main__":
    tree = BPTree(5)
    ok = True
    for x in range(100):
        list = [random.randint(1, 100) for i in range(1000)]
        random.shuffle(list)
        for i in list:
            tree.insert(i, 'x')
            tree.delete((i + 37) % 88)
        # print tree
        if tree.count_values() != tree.total: ok = False

    print ok
