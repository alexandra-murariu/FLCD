class LR:
    def __init__(self, g):
        self.g = g

    def goto(self, s, symbol):
        # s = [(S0, .S), (S, .aA)]
        if (symbol not in self.g.E) and (symbol not in self.g.N) and (symbol != self.g.S):
            raise ValueError("Symbol " + symbol + " is neither a terminal nor a nonterminal")

        result = []
        for item in s:
            point_pos = item[1].find('.')
            if symbol in item[1] and point_pos != len(item[1]) - 1 and point_pos != -1:
                if item[1][point_pos + 1] == symbol:
                    cur_item = list(item[1])
                    cur_item.remove('.')
                    cur_item.insert(point_pos + 1, '.')
                    result.append((item[0], ''.join(cur_item)))
        return result

    def closure(self, l):
        processed_nonterminals = []
        for item in l:
            point_pos = item[1].find('.')
            if point_pos != -1 and point_pos != len(item[1]) - 1:
                symbol = item[1][point_pos + 1]
                if symbol in self.g.N and symbol not in processed_nonterminals:
                    prods = self.g.prod_for_nonterminal(symbol)
                    for i in prods:
                        l.append((symbol, '.' + (i[0].replace(' ', ''))))
                    processed_nonterminals.append(symbol)
        return l

    def canonical_collection(self):
        set_of_states = []
        s0 = self.closure([('T', '.' + self.g.S)])
        self.g.enrich_grammar()
        set_of_states.append(s0)
        for s in set_of_states:
            for p in s:
                for i in range(len(p[1])):
                    if p[1][i] == '.' and i != len(p[1]) - 1:
                        new_s = self.closure(self.goto(s, p[1][i+1]))
                        if new_s not in set_of_states:
                            set_of_states.append(new_s)
        return set_of_states

    def print_canonical_collection(self, can_col):
        for i in range(len(can_col)):
            print("s" + str(i) + ":" + str(can_col[i]))
