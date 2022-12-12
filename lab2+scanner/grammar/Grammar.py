class Grammar:

    def __init__(self, filename):
        self.N = []
        self.E = []
        self.P = {}
        self.S = 'S'
        self.filename = filename
        self.read()

    def prod_for_nonterminal(self, nonTerminal):
        for key in self.P.keys():
            if key == nonTerminal:
                return self.P[key]

    def read(self):
        with open(self.filename, 'r') as file:
            self.N = [value.strip() for value in file.readline().strip().split(',')]
            self.E = [value.strip() for value in file.readline().strip().split(',')]
            self.S = file.readline().strip()
            rules = [value.strip() for value in ''.join([line for line in file]).strip().split(',')]
            i = 1

            for rule in rules:
                # print(rule)
                lhs, rhs = rule.split('->')
                lhs = lhs.strip()
                rhs = [value.strip() for value in rhs.split('|')]
                # print(rhs)
                for value in rhs:
                    if lhs in self.P.keys():
                        self.P[lhs].append((value, i))
                    else:
                        self.P[lhs] = [(value, i)]
                    i += 1
            # print("N: " + str(self.N))
            # print("S: " + str(self.S))
            # print("E: " + str(self.E))
            if not Grammar.validate(self.N, self.E, self.P, self.S):
                raise Exception("Wrong input file.")

    def is_cfg(self):
        for nonterminals in self.P.keys():
            if len(nonterminals.split()) > 1:
                return False
        return True

    @staticmethod
    def validate(N, E, P, S):
        if S not in N:
            print("S " + str(S) + "not in N " + str(N))
            return False
        for key in P.keys():
            for k in key.split():
                if k not in N:
                    print("K " + str(k) + "not in N " + str(N))
                    return False
            for move in P[key]:
                for ch in move[0].split():
                    # print("move " + str(move[0]))
                    # print("char " + str(char))
                    # for ch in char.split():
                    if ch not in N and ch not in E and ch != 'E':
                        print("!!!!!ch " + ch)
                        return False
        return True

    def __str__(self):
        return 'N = { ' + ', '.join(self.N) + ' }\n' \
               + 'E = { ' + ', '.join(self.E) + ' }\n' \
               + 'P = ' + str(self.P) + '\n' \
               + 'S = ' + str(self.S) + '\n'
