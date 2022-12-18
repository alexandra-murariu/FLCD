import unittest
from unittest import mock
from grammar.Grammar import Grammar
from grammar.console import GrammarConsole
from parser.LR import LR
from unittest.mock import patch, Mock


class TestLR(unittest.TestCase):
    def setUp(self) -> None:
        self.lr = LR(GrammarConsole("g_seminar.txt").g)

    def test_goto_normal_case(self):
        self.assertEqual(self.lr.goto([('S', 'a.A'), ('A', '.cA'), ('A', '.c')], 'c'), [('A', 'c.A'), ('A', 'c.')])

    def test_goto_empty_set(self):
        self.assertEqual(self.lr.goto([], 'A'), [])

    def test_goto_inexistent_symbol(self):
        with self.assertRaises(ValueError) as e:
            self.lr.goto([('S', 'a.A'), ('A', '.cA'), ('A', '.c')], 'z')
        self.assertEqual(str(e.exception), "Symbol z is neither a terminal nor a nonterminal")

    def test_goto_point_at_the_end(self):
        self.assertEqual(self.lr.goto([('S', 'aA.'), ('A', '.cA'), ('A', '.c')], 'c'), [('A', 'c.A'), ('A', 'c.')])

    def test_point_as_symbol(self):
        with self.assertRaises(ValueError) as e:
            self.lr.goto([('S', 'a.A'), ('A', '.cA'), ('A', 'c..')], '.')
        self.assertEqual(str(e.exception), "Symbol . is neither a terminal nor a nonterminal")

    def test_closure_normal_case(self):
        self.assertEqual(self.lr.closure([('A', 'c.A'), ('A', 'c.')]),
                         [('A', 'c.A'), ('A', 'c.'), ('A', '.bA'), ('A', '.c')])

    def test_closure_equal_to_initial_set(self):
        self.assertEqual(self.lr.closure([('S', 'aA.'), ('A', '.cA'), ('A', '.c')]),
                         [('S', 'aA.'), ('A', '.cA'), ('A', '.c')])

    def test_closure_recursive_closure(self):
        self.lr.g = Grammar("g_test.txt")
        self.assertEqual(self.lr.closure([('A', 'c.S'), ('A', '.c')]), [('A', 'c.S'),
                                                                        ('A', '.c'),
                                                                        ('S', '.BaA'),
                                                                        ('B', '.Aa'),
                                                                        ('A', '.bA'),
                                                                        ('A', '.c')])

    @mock.patch("parser.LR.LR.goto")
    @mock.patch("parser.LR.LR.closure")
    def test_can_col_normal_case(self, mock_closure, mock_goto):
        self.lr.g = Grammar("g_seminar.txt")
        mock_closure.side_effect = [[('T', '.S'), ('S', '.aA')], [('T', 'S.')],
                                    [('S', 'a.A'), ('A', '.bA'), ('A', '.c')], [('S', 'aA.')],
                                    [('A', 'b.A'), ('A', '.bA'), ('A', '.c')], [('A', 'c.')], [('A', 'bA.')],
                                    [('A', 'b.A'), ('A', '.bA'), ('A', '.c')], [('A', 'c.')]]
        mock_goto.side_effect = [[('T', 'S.')], [('S', 'a.A')], [('S', 'aA.')], [('A', 'b.A')], [('A', 'c.')],
                                 [('A', 'bA.')], [('A', 'b.A')], [('A', 'c.')]]
        can_col = self.lr.canonical_collection()
        self.assertEqual(mock_closure.call_count, 9)
        self.assertEqual(mock_goto.call_count, 8)
        set_can_col = set([tuple(x) for x in can_col])
        self.assertEqual(len(set_can_col), len(can_col))

    @mock.patch("parser.LR.LR.goto")
    @mock.patch("parser.LR.LR.closure")
    def test_raise_error_can_col(self, mock_closure, mock_goto):
        mock_closure.side_effect = ValueError("error")
        with self.assertRaises(ValueError) as e:
            self.lr.canonical_collection()
        self.assertEqual(str(e.exception), "error")


if __name__ == '__main__':
    unittest.main()
