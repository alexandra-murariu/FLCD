from tabulate import tabulate

from fa import console
from fa.console import Console
from grammar.console import GrammarConsole
from parser.LR import LR
from scanner import Scanner
from symbol_table import ST

if __name__ == "__main__":
    # st = ST.ST()
    # st.add("test")
    # st.add("ad")
    # st.add("bc")
    # st.add("2")
    # st.add("-5")
    # st.add('"message"')
    # st.add("'c'")
    # st.add("ad")  # doesn't add the same item twice
    # print("Hash Table: ")
    # print(st)
    # print("#######################")
    # print(st.find("ad"))
    # print(st.add("ad"))
    # print("#######################")
    # print("Symbol table: ")
    # print(tabulate(st.st_to_string()))
    #Scanner.Scanner("program3.txt", "tokens.in")
    c = GrammarConsole("g_seminar.txt")
    #c.run()
    lr = LR(c.g)
    # print(lr.goto([('S', 'a.A'), ('A', '.cA'), ('A', '.c')], 'c'))
    # print(lr.closure([('A', 'c.A'), ('A', 'c.')]))
    # s0 = lr.closure([('S0', '.S')])
    # s1 = lr.closure(lr.goto(s0, 'S'))
    # s2 = lr.closure(lr.goto(s0, 'a'))
    # s3 = lr.closure(lr.goto(s2, 'A'))
    # s4 = lr.closure(lr.goto(s2, 'b'))
    # print(s4)
    lr.print_canonical_collection(lr.canonical_collection())
    #print(lr.canonical_collection())
