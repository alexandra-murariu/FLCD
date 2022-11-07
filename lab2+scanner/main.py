from tabulate import tabulate

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
    s = Scanner.Scanner("program2.txt", "tokens.in")
