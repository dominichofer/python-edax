import unittest
from edax.binary import Edax, MultiprocessEdax


class EdaxTest(unittest.TestCase):
    def test_name(self):
        self.assertEqual(Edax.name(), "Edax version 4.4")

    def test_solve_one(self):
        engine = Edax()
        result = engine.solve("--XXXXX--OOOXX-O-OOOXXOX-OXOXOXXOXXXOXXX--XOXOXX-XXXOOO--OOOOO-- X")
        self.assertEqual(result.lines[0].score, +18)

    def test_solve_many(self):
        engine = Edax()
        result = engine.solve(
            ["--XXXXX--OOOXX-O-OOOXXOX-OXOXOXXOXXXOXXX--XOXOXX-XXXOOO--OOOOO-- X"] * 10
        )
        self.assertEqual(len(result.lines), 10)
        for line in result.lines:
            self.assertEqual(line.score, +18)


class MultiprocessEdaxTest(unittest.TestCase):
    def test_name(self):
        self.assertEqual(MultiprocessEdax.name(), "Edax version 4.4")

    def test_solve_one(self):
        engine = MultiprocessEdax()
        result = engine.solve("--XXXXX--OOOXX-O-OOOXXOX-OXOXOXXOXXXOXXX--XOXOXX-XXXOOO--OOOOO-- X")
        self.assertEqual(result[0].score, +18)

    def test_solve_many(self):
        engine = MultiprocessEdax()
        result = engine.solve(
            ["--XXXXX--OOOXX-O-OOOXXOX-OXOXOXXOXXXOXXX--XOXOXX-XXXOOO--OOOOO-- X"] * 10
        )
        self.assertEqual(len(result), 10)
        for r in result:
            self.assertEqual(r.score, +18)
