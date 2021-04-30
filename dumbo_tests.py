import unittest

import dumbo_interpreter as dumbo


class TestClass(unittest.TestCase):
    def test_expression_for(self):
        data = "{{numbers := ('0', '1', '2', '3');}}"
        template = "{{for num in numbers do print num . ' ';" \
                   "endfor;}}"
        self.assertEqual("0 1 2 3 ", dumbo.interpret(data, template))

    def test_get_int(self):
        data = "{{i := 0;}}"
        template = "{{print i;}}"
        self.assertEqual("0", dumbo.interpret(data, template))

    def test_get_str(self):
        data = "{{nom := 'Perla';}}"
        template = "{{print nom;}}"
        self.assertEqual("Perla", dumbo.interpret(data, template))

    def test_add_expr(self):
        data = "{{add := 2 + 3;}}"
        template = "{{print add;}}"
        self.assertEqual("5", dumbo.interpret(data, template))

    def test_sub_expr(self):
        data = "{{sub := 5 - 2;}}"
        template = "{{print sub;}}"
        self.assertEqual("3", dumbo.interpret(data, template))

    def test_multi_expr(self):
        data = "{{multi := 2 * 3;}}"
        template = "{{print multi;}}"
        self.assertEqual("6", dumbo.interpret(data, template))

    def test_div_expr(self):
        data = "{{div := 6 / 3;}}"
        template = "{{print div;}}"
        self.assertEqual("2", dumbo.interpret(data, template))

    def test_math_expr(self):
        data = "{{sub := 5 - 2 * 3;}}"
        template = "{{print sub;}}"
        self.assertEqual("-1", dumbo.interpret(data, template))

    def test_math_par(self):
        data = "{{sub := (5 - 2) * 3;}}"
        template = "{{print sub;}}"
        self.assertEqual("9", dumbo.interpret(data, template))

    def test_if_not_equal(self):
        data = "{{}}"
        template = "{{if 1 != 2 do print 'bravo'; endif;}}"
        self.assertEqual("bravo", dumbo.interpret(data, template))

    def test_if_equal(self):
        data = "{{}}"
        template = "{{if 2 = 2 do print 'bravo'; endif;}}"
        self.assertEqual("bravo", dumbo.interpret(data, template))

    def test_if_upper(self):
        data = "{{}}"
        template = "{{if 3 > 2 do print 'bravo'; endif;}}"
        self.assertEqual("bravo", dumbo.interpret(data, template))

    def test_if_lower(self):
        data = "{{}}"
        template = "{{if 1 < 2 do print 'bravo'; endif;}}"
        self.assertEqual("bravo", dumbo.interpret(data, template))

    def test_if_and(self):
        data = "{{}}"
        template = "{{if 1 < 2 and 1 = 1 do print 'bravo'; endif;}}"
        self.assertEqual("bravo", dumbo.interpret(data, template))

    def test_if_or(self):
        data = "{{}}"
        template = "{{if 1 < 2 or 1 = 2 do print 'bravo'; endif;}}"
        self.assertEqual("bravo", dumbo.interpret(data, template))

    def test_concat(self):
        data = "{{hi := 'hello' . ' world';}}"
        template = "{{print hi;}}"
        self.assertEqual("hello world", dumbo.interpret(data, template))

if __name__ == '__main__':
    unittest.main()
