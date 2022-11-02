import re

from tabulate import tabulate

from symbol_table.ST import ST


class Scanner:
    def __init__(self, filename, tokenfile):
        self.filename = filename
        self.tokenfile = tokenfile
        self._st = ST()
        self._pif = []
        self.tokens = []
        self.read_tokens()
        try:
            self.scan()
            self.write_to_file()
        except ValueError as e:
            print(e)

    def read_tokens(self):
        with open(self.tokenfile, "r") as f:
            self.tokens = f.read().split()

    def scan(self):
        lines = []
        with open(self.filename, "r") as f:
            for line in f:
                lines.append(line.split())
        for parts in lines:
            for part in parts:
                elements = self.find_tokens(part)
                for elem in elements:
                    if elem in self.tokens:
                        self._pif.append((elem, -1))
                    elif self.is_identifier(elem):
                        self._st.add(elem)
                        self._pif.append(('identifier', self._st.find(elem)[0].key))
                    elif self.is_constant(elem):
                        self._st.add(elem)
                        self._pif.append(('constant', self._st.find(elem)[0].key))
                    else:
                        raise ValueError('Lexical Error: line ' + str(lines.index(parts) + 1) + ' at token ' + elem)

        # print(self.tokens)
        # print(self._pif)
        # print(self._st.st_to_string())
        # for token in token_parts:
        #     self.validate_token()

    def is_identifier(self, elem):
        if elem != "true" and elem != "false" and re.match('^[_a-zA-Z]+[a-zA-Z0-9_]*$', elem) is not None:
            return True
        return False

    def find_tokens(self, string):
        line_data = re.split('("[^_a-zA-Z0-9\"\']")|([^_a-zA-Z0-9\"\'])', string)
        print(str(string) + ":" + str(line_data))
        elements = [el for el in line_data if el is not None and el != '' and el != ' ']
        for i in range(len(elements) - 1):
            if elements[i] == "=" and elements[i + 1] == "=":
                elements[i] += elements[i + 1]
                del elements[i + 1]
            elif elements[i] == "<" and elements[i + 1] == "=":
                elements[i] += elements[i + 1]
                del elements[i + 1]
            elif elements[i] == ">" and elements[i + 1] == "=":
                elements[i] += elements[i + 1]
                del elements[i + 1]
            elif elements[i] == "!" and elements[i + 1] == "=":
                elements[i] += elements[i + 1]
                del elements[i + 1]
        return elements

    def is_constant(self, elem):
        if (
                re.match('^\"[a-zA-Z0-9-_ ]+\"$', elem) is not None) or (  # string
                re.match('^\'[a-zA-Z0-9\-_ ]\'$', elem) is not None) or (  # char
                re.match('^[1-9][0-9]*$|^0$', elem) is not None) or (  # number
                re.match('^true|false$', elem) is not None):  # bool
            return True
        return False

    def write_to_file(self):
        with open('PIF.out', 'w') as file:
            file.write(tabulate(self._pif))
        with open('ST.out', 'w') as file:
            file.write("hashtable\n")
            file.write(tabulate(self._st.st_to_string()))
