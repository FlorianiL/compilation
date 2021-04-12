from lark import Lark
from lark.visitors import Interpreter, Transformer
import operator


class TreeToDumbo(Interpreter):
    OPERATORS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.floordiv,
        '<': operator.lt,
        '<=': operator.le,
        '>': operator.gt,
        '>=': operator.ge,
        '!=': operator.ne,
        '=': operator.eq,
    }

    def __init__(self):
        self.result = ""
        self.variables = {}

    def start(self, tree):  # OK
        self.visit_children(tree)

    def program(self, tree):  # OK
        self.visit_children(tree)

    def txt(self, tree):  # OK
        res = tree.children[0].value
        self.result += res

    def dumbo_block(self, tree):  # OK
        self.visit_children(tree)

    def expression_list(self, tree):  # OK
        self.visit_children(tree)

    def expression(self, tree):  # OK
        self.visit_children(tree)

    def expression_var(self, tree):  # OK
        name, value = self.visit_children(tree)
        self.variables[name] = value

    def expression_print(self, tree):  # OK
        to_print = self.visit_children(tree)
        self.result += to_print[0]

    def expression_for_lis(self, tree):  # OK
        variable_set, string_list, expressions_list = tree.children
        self.expression_for(variable_set, string_list, expressions_list)

    def expression_for_var(self, tree):  # OK
        variable_set, variable_get, expressions_list = tree.children
        self.expression_for(variable_set, variable_get, expressions_list)

    def expression_for(self, variable_set, list_or_get, expressions_list):
        list = self.visit(list_or_get)
        name = self.visit_children(variable_set)[0]
        for value in list:
            self.variables[name] = value
            self.visit_children(expressions_list)

    def expression_if(self, tree):  # TODO A TESTER
        test, expression_list = tree.children
        bool = self.visit_children(test)
        if bool:
            self.visit_children(expression_list)

    def string_expression(self, tree):  # OK
        token = self.visit_children(tree)[0]
        return token

    def string_concat(self, tree):  # OK
        str1, str2 = self.visit_children(tree)
        return str1[1:-1] + str2[1:-1]

    def string_list(self, tree):  # OK
        return self.visit_children(tree)[0]

    def string_list_interior(self, tree):  # OK
        if len(tree.children) == 1:
            # end of the list
            return self.visit_children(tree)
        elif len(tree.children) == 2:
            return [self.visit(tree.children[0])] + self.visit(tree.children[1])

    def test(self, tree):  # TODO A TESTER
        if len(tree.children) == 1:
            self.visit_children(tree)
        elif len(tree.children) == 2:
            test_, and_test = tree.children
            return self.visit_children(test_) or self.visit_children(and_test)

    def and_test(self, tree):  # TODO A TESTER
        if len(tree.children) == 1:
            self.visit_children(tree)
        elif len(tree.children) == 2:
            and_test, comparison = tree.children
            return self.visit_children(and_test) and self.visit_children(comparison)

    def comparison(self, tree):  # TODO
        pass

    def arith_expression(self, tree):  # TODO
        pass

    def term(self, tree):  # TODO
        pass

    def factor(self, tree):  # TODO A TESTER
        self.visit_children(tree)

    def variable_set(self, tree):  # OK
        name = self.visit_children(tree)[0].value
        return name

    def variable_get_str(self, tree):  # TODO A TESTER
        self.variable_get(tree)

    def variable_get_int(self, tree):  # TODO A TESTER
        self.variable_get(tree)

    def variable_get(self, tree):  # OK
        name = self.visit_children(tree)[0].value
        try:
            return self.variables[name]
        except KeyError:
            raise Exception("Variable not found: %s" % name)

    def string(self, tree):  # OK
        str = tree.children[0].value
        res = str[1:-1]
        return res

    def boolean(self, tree):  # TODO A TESTER
        bools = {"true": True,
                 "false": False}
        bool = tree.children[0].value
        return bools[bool]

    # FONCTIONS UTILITAIRES
    def get_vars(self, tree):
        self.visit(tree)
        return self.variables

    def construct(self, tree, variables_):
        self.variables = variables_
        self.visit(tree)
        print(self.result)


def test_lark(data, template):
    grammar = open("../src/dumbo.lark", "r").read()
    tree_data = Lark(grammar, parser='lalr', propagate_positions=True, debug=True).parse(data.read())
    tree_template = Lark(grammar, parser='lalr', propagate_positions=True, debug=True).parse(template.read())
    TreeToDumbo().construct(tree_template, TreeToDumbo().get_vars(tree_data))
