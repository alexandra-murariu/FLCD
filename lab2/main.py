from tabulate import tabulate


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
            return key
        else:
            while node.next is not None:
                node = node.next
            node.next = Node(key, value)
            return key

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


class ST:
    def __init__(self):
        self._current_key = 0
        self._table = HashTable(23)
        self._values = []

    def add(self, value):
        if self._table.get(value) is None:
            self._values.append([self._current_key, value])
        val = self._table.insert(self._current_key, value)
        self._current_key += 1
        return val

    def find(self, value):
        result = self._table.get(value)
        return str(result[0]) + " -> container " + str(result[1])

    def __str__(self):
        return str(self._table)

    def st_to_string(self):
        table = []
        return self._values


if __name__ == "__main__":
    st = ST()
    st.add("test")
    st.add("ad")
    st.add("bc")
    st.add("2")
    st.add("-5")
    st.add('"message"')
    st.add("'c'")
    st.add("ad")  # doesn't add the same item twice
    print("Hash Table: ")
    print(st)
    print("#######################")
    print(st.find("ad"))
    print(st.add("ad"))
    print("#######################")
    print("Symbol table: ")
    print(tabulate(st.st_to_string()))
