from grammar.Grammar import Grammar


class GrammarConsole:
    def __init__(self, filename):
        self.g = Grammar(filename)

    def print_menu(self):
        print("1.Grammar")
        print("2.Nonterminals")
        print("3.Terminals")
        print("4.Productions")
        print("5.Productions for a given nonterminal")
        print("6.Check CFG")
        print("x: exit")

    def run(self):
        while True:
            self.print_menu()
            cmd = input()
            if cmd == '1':
                print(self.g)
            elif cmd == '2':
                print(self.g.N)
            elif cmd == '3':
                print(self.g.E)
            elif cmd == '4':
                print(self.g.P)
            elif cmd == '5':
                print(self.g.prod_for_nonterminal(input()))
            elif cmd == '6':
                print(self.g.is_cfg())
            elif cmd == 'x':
                break
            else:
                print("Wrong command! Please try again")
