import copy
from lib2to3.pytree import Node

import lark.tree
from lark import Lark
from lark.visitors import Interpreter, Transformer

class TreeToDumbo(Interpreter):

    def __init__(self):
        self.result = ""
        self.variables = {}
        self.list_strings = []
        self.list_expr = []

    def start(self, tree):
        # print(f"start --> {tree}")
        self.visit_children(tree)

    def program(self, tree):
        # print(f"program --> {tree}")
        self.visit_children(tree)

    def dumbo_block(self, tree):
        # print(f"dumbo_block --> {tree}")
        self.list_strings = []
        self.list_expr = []
        self.visit_children(tree)

    def expression_list(self, tree):
        # print(f"expression_list {tree}")
        self.visit_children(tree)

    def expression(self, tree):
        # print(f"expression --> {tree}")
        self.visit_children(tree)

    def expression_print(self, tree):  # OK
        to_print = self.visit_children(tree)
        # print(f"expression_print --> {to_print}")
        self.result += to_print[0]

    def expression_for_lis(self, tree):
        # print(f"expression_for_lis --> {tree}")
        variable_set, string_list, expressions_list = tree.children
        list = self.visit(string_list)
        name = self.visit_children(variable_set)[0]
        for value in list:
            self.variables[name] = value
            self.visit_children(expressions_list)

    def expression_for_var(self, tree):
        # print(f"expression_for_var --> {tree}")
        variable_set, variable_get, expressions_list = tree.children
        list = self.visit(variable_get)
        name = self.visit_children(variable_set)[0]
        for value in list:
            self.variables[name] = value
            self.visit_children(expressions_list)

    def expression_var(self, tree):
        name, value = self.visit_children(tree)
        # print(f"expression_var --> name : {name} & value : {value}")
        self.variables[name] = value

    def string_expression(self, tree):
        token = self.visit_children(tree)[0]
        # print(f"string_expression --> {token}")
        return token

    def string_concat(self, tree):                          # ATTENTION NOT TESTED
        str1, str2 = self.visit_children(tree)
        # print(f"string_concat --> {tree}")
        return str1[1:-1] + str2[1:-1]

    def string_list(self, tree):
        # print(f"string_list --> {tree}")
        return self.visit_children(tree)[0]

    def string_list_interior(self, tree):
        # print(f"string_list_interior --> {tree}")
        if len(tree.children) == 1:
            # end of the list
            return self.visit_children(tree)
        elif len(tree.children) == 2:
            return [self.visit(tree.children[0])] + self.visit(tree.children[1])

    def variable_get(self, tree):
        # print(f"variable_get --> {tree}")
        name = self.visit_children(tree)[0].value
        try:
            return self.variables[name]
        except KeyError:
            raise Exception("Variable not found: %s" % name)

    def variable_set(self, tree):
        name = self.visit_children(tree)[0].value
        # print(f"variable_set ---> {name}")
        return name

    def string(self, tree):
        s = tree.children[0].value
        res = s[1:-1]
        # print(f"string --> {res}")
        return res

    def txt(self, tree):
        res = tree.children[0].value
        # print(f"txt --> {res}")
        self.result += res

    def get_vars(self, tree):
        self.visit(tree)
        return self.variables

    def construct(self, tree, variables_):
        self.variables = variables_
        self.visit(tree)
        print(self.result)


def test_lark(data, template):
    grammar = open("../src/dumbo.lark", "r").read()
    tree_data = Lark(grammar, parser='lalr', propagate_positions=True).parse(data.read())
    tree_template = Lark(grammar, parser='lalr', propagate_positions=True).parse(template.read())
    TreeToDumbo().construct(tree_template, TreeToDumbo().get_vars(tree_data))
