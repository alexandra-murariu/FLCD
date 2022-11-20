class FiniteAutomata:

    def __init__(self, filename):
        self.states = []
        self.alphabet = []
        self.initial_state = 'q'
        self.final_states = []
        self.transitions = {}
        self.filename = filename
        self.read()

    def is_dfa(self):
        for k in self.transitions.keys():
            if len(self.transitions[k]) > 1:
                return False
        return True

    def is_seq_accepted(self, seq):
        if not self.is_dfa():
            return False
        crt = self.initial_state
        for symbol in seq:
            if (crt, symbol) not in self.transitions.keys():
                return False
            crt = self.transitions[(crt, symbol)][0]
        return crt in self.final_states

    def read(self):
        with open(self.filename) as file:
            states = file.readline().strip().split(' ')
            alphabet = file.readline().strip().split(' ')
            initial_state = file.readline().strip().split(' ')[0]
            final_states = file.readline().strip().split(' ')
            transitions = {}

            for line in file:
                source = line.strip().split('->')[0].strip().replace('(', '').replace(')', '').split(',')[0]
                symbol = line.strip().split('->')[0].strip().replace('(', '').replace(')', '').split(',')[1]
                destination = line.strip().split('->')[1].strip()

                if (source, symbol) in transitions.keys():
                    transitions[(source, symbol)].append(destination)
                else:
                    transitions[(source, symbol)] = [destination]

            if initial_state not in states:
                raise Exception("Something is wrong.")

            for f in final_states:
                if f not in states:
                    raise Exception("Something is wrong.")
            for key in transitions.keys():
                state = key[0]
                symbol = key[1]
                if state not in states:
                    raise Exception("Something is wrong.")
                if symbol not in alphabet:
                    raise Exception("Something is wrong.")
                for dest in transitions[key]:
                    if dest not in states:
                        raise Exception("Something is wrong.")

            self.states = states
            self.transitions = transitions
            self.initial_state = initial_state
            self.alphabet = alphabet
            self.final_states = final_states

    def __str__(self):
        return "Q = { " + ', '.join(self.states) + " }\n" \
                                                   "E = { " + ', '.join(self.alphabet) + " }\n" \
                                                                                         "q0 = { " + self.initial_state + " }\n" \
                                                                                                                          "F = { " + ', '.join(
            self.final_states) + " }\n" \
                                 "S = { " + str(self.transitions) + " } "
