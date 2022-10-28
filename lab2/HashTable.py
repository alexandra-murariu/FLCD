class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __str__(self):
        return str(self.key) + ": " + str(self.value)


class HashTable:
    def __init__(self, initial_capacity):
        self._capacity = initial_capacity
        self._size = 0
        self._containers = [None] * self._capacity

    def hash(self, value):
        ascii_sum = 0
        for c in value:
            ascii_sum += ord(c)
        return ascii_sum % self._capacity

    def insert(self, key, value):
        self._size += 1
        idx = self.hash(value)
        node = self._containers[idx]
        if self.get(value) is not None:
            return self.get(value)[0].key, self.get(value)[1]
        if node is None:
            self._containers[idx] = Node(key, value)
            return idx, key
        else:
            while node.next is not None:
                node = node.next
            node.next = Node(key, value)
            return idx, key

    def get(self, value):
        idx = self.hash(value)
        node = self._containers[idx]
        while node is not None and node.value != value:
            node = node.next
        if node is None:
            return None
        else:
            return node, idx

    def __str__(self):
        hash_table_string = ""
        for i in range(len(self._containers)):
            node = self._containers[i]
            hash_table_string += "container nr. " + str(i) + " -> "
            while node is not None:
                hash_table_string += str(node)
                hash_table_string += "; "
                node = node.next
            hash_table_string += "\n"
        return hash_table_string