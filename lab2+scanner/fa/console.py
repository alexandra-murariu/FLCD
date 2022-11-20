from fa.FiniteAutomata import FiniteAutomata


class Console:
    def __init__(self, filename):
        self.fa = FiniteAutomata(filename)

    def print_menu(self):
        print("1.FA")
        print("2.FA States")
        print("3.FA Alphabet")
        print("4.FA transitions")
        print("5.FA final states")
        print("6.Check DFA")
        print("7.Check accepted sequence")
        print("x: exit")

    def run(self):
        while True:
            self.print_menu()
            cmd = input()
            if cmd == '1':
                print(self.fa)
            elif cmd == '2':
                print(self.fa.states)
            elif cmd == '3':
                print(self.fa.alphabet)
            elif cmd == '4':
                print(self.fa.transitions)
            elif cmd == '5':
                print(self.fa.final_states)
            elif cmd == '6':
                print(self.fa.is_dfa())
            elif cmd == '7':
                print(self.fa.is_seq_accepted(input()))
            elif cmd == 'x':
                break
            else:
                print("Wrong command! Please try again")
