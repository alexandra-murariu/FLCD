from tabulate import tabulate


class LR:
    def __init__(self, g):
        self.g = g

    def goto(self, s, symbol, idx):
        if (symbol not in self.g.E) and (symbol not in self.g.N) and (symbol != self.g.S):
            raise ValueError("Symbol " + symbol + " is neither a terminal nor a nonterminal")

        result = []
        for item in s:
            point_pos = item[1].find('.')
            if symbol in item[1] and point_pos != len(item[1]) - 1 and point_pos != -1:
                if item[1][point_pos + 1: point_pos + 1 + len(symbol)] == symbol:
                    cur_item = list(item[1])
                    cur_item.remove('.')
                    cur_item.insert(point_pos + len(symbol), '.')
                    result.append((item[0], ''.join(cur_item)))
        return result

    def closure(self, l):
        processed_nonterminals = []
        for item in l:
            point_pos = item[1].find('.')
            if point_pos != -1 and point_pos != len(item[1]) - 1:
                symbol = item[1][point_pos + 1]
                if symbol not in self.g.N and symbol not in self.g.E and symbol != self.g.S:
                    j = point_pos + 1
                    while symbol not in self.g.N and symbol not in self.g.E and symbol != self.g.S:
                        symbol += item[1][j + 1]
                        j = j + 1
                if symbol in self.g.N and symbol not in processed_nonterminals:
                    prods = self.g.prod_for_nonterminal(symbol)
                    if prods:
                        for i in prods:
                            l.append((symbol, '.' + (i[0].replace(' ', ''))))
                    processed_nonterminals.append(symbol)
        return l

    def canonical_collection(self):
        set_of_states = []
        s0 = self.closure([('T', '.' + self.g.S)])
        self.g.enrich_grammar()
        set_of_states.append(s0)
        set_of_gotos = []
        for idx, s in enumerate(set_of_states):
            for p in s:
                for i in range(len(p[1])):
                    if p[1][i] == '.' and i != len(p[1]) - 1:
                        if (p[1][i + 1] not in self.g.E) and (p[1][i + 1] not in self.g.N) and (
                                p[1][i + 1] != self.g.S):
                            sym = p[1][i + 1]
                            j = i + 1
                            while sym not in self.g.E and sym not in self.g.N and sym != self.g.S:
                                sym += p[1][j + 1]
                                j += 1
                        else:
                            sym = p[1][i + 1]
                        new_s = self.closure(self.goto(s, sym, idx))
                        if new_s not in set_of_states:
                            set_of_gotos.append((idx, sym, len(set_of_states)))
                            set_of_states.append(new_s)
                        else:
                            set_of_gotos.append((idx, sym, set_of_states.index(new_s)))
                        break
        return set_of_states, set_of_gotos

    def print_canonical_collection(self, can_col):
        for i in range(len(can_col)):
            print("s" + str(i) + ":" + str(can_col[i]))

    def compute_parsing_table(self, can_col):
        parsing_table = {}
        list_of_symbols = self.g.E + self.g.N
        set_of_states = can_col[0]
        set_of_gotos = can_col[1]
        for idx_of_s, s in enumerate(set_of_states):
            row_for_s = {'action': ''}
            for symbol in list_of_symbols:
                row_for_s[symbol] = 'error'
            for elem in s:
                if elem == ('T', 'S.') or elem == ('T', 'P.'):
                    row_for_s['action'] = 'acc'
            if row_for_s['action'] != 'acc':
                for i, t in enumerate(set_of_gotos):
                    if t[0] == idx_of_s:
                        row_for_s['action'] = 'shift'
                        row_for_s[t[1]] = 's' + str(t[2])
                for prod in s:
                    if prod[1][len(prod[1]) - 1] == '.':
                        prod_rhs = prod[1].replace('.', '')
                        if prod[0] in self.g.P.keys():
                            for p in self.g.P[prod[0]]:
                                if p[0].replace(" ", "") == prod_rhs:
                                    if row_for_s['action'] == 'shift':
                                        raise ValueError("Shift reduce conflict at ", idx_of_s, p, prod[0])
                                    elif 'reduce' in row_for_s['action']:
                                        raise ValueError("Reduce reduce conflict at ", idx_of_s)
                                    row_for_s['action'] = 'reduce ' + str(p[1])
            parsing_table['s' + str(idx_of_s)] = row_for_s
        return parsing_table

    def parse_sequence(self, seq_file, parsing_table):
        w = ''
        with open(seq_file, 'r') as file:
            for line in file:
                w = line
                break
        work_stack = [('$', 's0')]
        if "PIF" in seq_file:
            input_stack = w.split()
        else:
            input_stack = [l for l in w]
        output_band = []
        tree_stack = []
        parsing_tree = []
        current_idx = 0
        while input_stack or work_stack:
            table_row = parsing_table[work_stack[-1][1]]
            if table_row['action'] == 'shift':
                token = input_stack[0]
                if table_row[token] == 'error':
                    raise ValueError(
                        "Error at state " + work_stack[-1][1] + " and symbol " + token + " with row " + str(table_row))
                work_stack.append((token, table_row[token]))
                input_stack.pop(0)
                tree_stack.append((token, current_idx))
                current_idx += 1
            elif table_row['action'] == 'acc':
                last_in_tree = tree_stack[-1]
                del tree_stack[-1]
                parsing_tree.append((last_in_tree[1], last_in_tree[0], -1, -1))
                return parsing_tree
            elif 'reduce' in table_row['action']:
                reduce_prod = []
                for key, val in self.g.P.items():
                    for prod in val:
                        if str(prod[1]) == str(table_row['action'].split()[1]):
                            reduce_prod = [key, prod]
                parent_idx = current_idx
                current_idx += 1
                last_idx = -1
                for j in range(len(reduce_prod[1][0].split())):
                    del work_stack[-1]
                    last_in_tree = tree_stack[-1]
                    del tree_stack[-1]
                    parsing_tree.append((last_in_tree[1], last_in_tree[0], parent_idx, last_idx))
                    last_idx = last_in_tree[1]
                tree_stack.append((reduce_prod[0], parent_idx))
                last_in_ws = work_stack[-1]
                if parsing_table[last_in_ws[1]][reduce_prod[0]] == 'error':
                    raise ValueError("Error at state " + work_stack[-1][1] + " and symbol " + reduce_prod[0])
                work_stack.append((reduce_prod[0], parsing_table[last_in_ws[1]][reduce_prod[0]]))
                output_band.insert(0, reduce_prod[1][1])
            else:
                raise ValueError("Error at state " + work_stack[-1][1] + " with row " + str(table_row))

    def print_tree(self, node_info, file_name):
        print(tabulate(node_info, headers=["idx", "info", "parent", "right sibling"], tablefmt="fancy_grid"))
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(tabulate(node_info, headers=["idx", "info", "parent", "right sibling"], tablefmt="fancy_grid"))
