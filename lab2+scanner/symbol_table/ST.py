from symbol_table.HashTable import HashTable


class ST:
    def __init__(self):
        self._current_key = 0
        self._table = HashTable(23)
        self._values = []

    def add(self, value):
        if self._table.get(value) is None:
            self._values.append([self._current_key, value])
        else:
            return self._table.get(value)
        val = self._table.insert(self._current_key, value)
        self._current_key += 1
        return val

    def find(self, value):
        result = self._table.get(value)
        return result

    def __str__(self):
        return str(self._table)

    def st_to_string(self):
        return self._values
