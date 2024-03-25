import unittest
from edax.output import Line, Output


class EdaxLineTest(unittest.TestCase):
    def test_exact_depth(self):
        string = "  7|   24   -08        0:00.234      63133975  269803312 b3 C1 b1 A3 b2 H3 a5"
        line = Line(string)
        self.assertEqual(line.index, 7)
        self.assertEqual(line.depth, 24)
        self.assertEqual(line.selectivity, None)
        self.assertEqual(line.score, -8)
        self.assertEqual(line.time, "0:00.234")
        self.assertEqual(line.nodes, 63133975)
        self.assertEqual(line.nodes_per_second, 269803312)
        self.assertEqual(line.pv, ["b3", "C1", "b1", "A3", "b2", "H3", "a5"])
        self.assertEqual(str(line), string)

    def test_depth_selectivity(self):
        string = "  8|25@98%  +03        0:00.094       9940593  105750989 G2 b8 B7 a2 A5 b2 G3"
        line = Line(string)
        self.assertEqual(line.index, 8)
        self.assertEqual(line.depth, 25)
        self.assertEqual(line.selectivity, 98)
        self.assertEqual(line.score, +3)
        self.assertEqual(line.time, "0:00.094")
        self.assertEqual(line.nodes, 9940593)
        self.assertEqual(line.nodes_per_second, 105750989)
        self.assertEqual(line.pv, ["G2", "b8", "B7", "a2", "A5", "b2", "G3"])
        self.assertEqual(str(line), string)

    def test_no_nodes_per_second(self):
        string = "  1|   14   +18        0:00.000         95959            g8 H7 a8 A6 a4 A7 b6"
        line = Line(string)
        self.assertEqual(line.index, 1)
        self.assertEqual(line.depth, 14)
        self.assertEqual(line.selectivity, None)
        self.assertEqual(line.score, +18)
        self.assertEqual(line.time, "0:00.000")
        self.assertEqual(line.nodes, 95959)
        self.assertEqual(line.nodes_per_second, None)
        self.assertEqual(line.pv, ["g8", "H7", "a8", "A6", "a4", "A7", "b6"])
        self.assertEqual(str(line), string)

    def test_pass(self):
        string = "  7|   24   -08        0:00.234      63133975  269803312 ps"
        line = Line(string)
        self.assertEqual(line.index, 7)
        self.assertEqual(line.depth, 24)
        self.assertEqual(line.selectivity, None)
        self.assertEqual(line.score, -8)
        self.assertEqual(line.time, "0:00.234")
        self.assertEqual(line.nodes, 63133975)
        self.assertEqual(line.nodes_per_second, 269803312)
        self.assertEqual(line.pv, ["ps"])
        self.assertEqual(str(line), string)


class EdaxOutputTest(unittest.TestCase):
    def setUp(self) -> None:
        self.string = (
            " # | depth|score|       time   |  nodes (N)  |   N/s    | principal variation\n"
            "---+------+-----+--------------+-------------+----------+---------------------\n"
            "  1|   14   +18        0:00.000         95808            g8 H7 a8 A6 a4 A7 b6\n"
            "  2|   14   +10        0:00.000         33248            a4 B7 a3 A2 b8 A7 g7\n"
            "  3|   14   +02        0:00.000        158039            d1 G1 b8 C1 g3 A8 g2\n"
            "  4|   14   +00        0:00.000         37328            h8 B6 a7 H7 g7 A5 b7\n"
            "  5|   14   +32        0:00.000         14824            g8 G7 h8 G2 b2 A2 a1\n"
            "  6|   14   +14        0:00.000         62426            a1 B1 h3 H4 h6 H2 h1\n"
            "  7|   14   +08        0:00.000         22466            a6 C8 b7 A7 a8 B8 h8\n"
            "  8|   15   +08        0:00.000        298442            E1 h7 H6 g7 H8 g8 H2\n"
            "  9|   15   -08        0:00.000         67314            G7 a7 A4 h7 H1 g1 H8\n"
            " 10|   15   +10        0:00.000        148812            B2 b7 G1 g8 H8 g7 H7\n"
            " 11|   15   +30        0:00.000         71198            B3 a3 A6 c3 B4 ps A2\n"
            " 12|   15   -08        0:00.000        134142            B7 h2 A7 a8 H1 g1 B2\n"
            " 13|   16   +14        0:00.000        121971            b7 H7 h8 A8 g8 G2 a7\n"
            " 14|   16   +18        0:00.000        116636            a3 B7 a4 B2 b1 G2 a1\n"
            " 15|   16   +04        0:00.015        514787   34319133 g3 F1 c1 D1 b8 A8 g1\n"
            " 16|   16   +24        0:00.016        246403   15400188 f8 B6 a7 C7 h1 G7 h7\n"
            " 17|   16   +08        0:00.000         35325            f8 F7 g8 H3 h7 B7 b2\n"
            " 18|   16   -02        0:00.000        212374            g2 B7 a8 A7 g8 H1 f1\n"
            " 19|   16   +08        0:00.000        198926            b6 B5 a6 C8 b7 A7 a8\n"
            "------+-----+--------------+-------------+----------+---------------------\n"
            "fforum-1-19.obf: 2590469 nodes in  0:00.031 (83563516 nodes/s).\n"
            "19 positions; 0 erroneous move; 0 erroneous score; "
            "mean absolute score error = 0.000; mean absolute move error = 0.000\n"
        )
        self.output = Output(self.string)

    def test_string(self):
        self.assertEqual(self.output.string, self.string)

    def test_lines(self):
        self.assertEqual(len(self.output.lines), 19)

    def test_nodes(self):
        self.assertEqual(self.output.nodes, 2590469)

    def test_time(self):
        self.assertEqual(self.output.time, "0:00.031")

    def test_nodes_per_second(self):
        self.assertEqual(self.output.nodes_per_second, 83563516)

    def test_no_nodes_per_second(self):
        string = (
            " # | depth|score|       time   |  nodes (N)  |   N/s    | principal variation\n"
            "---+------+-----+--------------+-------------+----------+---------------------\n"
            "  1|   14   +18        0:00.000         95808            g8 H7 a8 A6 a4 A7 b6\n"
            "------+-----+--------------+-------------+----------+---------------------\n"
            "fforum-1-19.obf: 2590469 nodes in  0:00.000\n"
            "19 positions; 0 erroneous move; 0 erroneous score; "
            "mean absolute score error = 0.000; mean absolute move error = 0.000\n"
        )
        output = Output(string)
        self.assertEqual(output.time, "0:00.000")
        self.assertEqual(output.nodes_per_second, None)

    def test_little_nodes_per_second(self):
        string = (
            " # | depth|score|       time   |  nodes (N)  |   N/s    | principal variation\n"
            "---+------+-----+--------------+-------------+----------+---------------------\n"
            "  1|   14   +18        0:00.000         95808            g8 H7 a8 A6 a4 A7 b6\n"
            "------+-----+--------------+-------------+----------+---------------------\n"
            "fforum-1-19.obf: 2590469 nodes in  0:00.031 ( 1 nodes/s).\n"
            "19 positions; 0 erroneous move; 0 erroneous score; "
            "mean absolute score error = 0.000; mean absolute move error = 0.000\n"
        )
        output = Output(string)
        self.assertEqual(output.nodes_per_second, 1)
