import copy
from lib2to3.pytree import Node

import lark.tree
from lark import Lark
from lark import Transformer

calc_grammar = """
    start : program
    
    program : txt
            | txt program
            | dumbo_block
            | dumbo_block program
    
    txt : /[a-zA-Z0-9 \/\\ \n\s _;&<>"-.:,]+/x
    
    dumbo_block : ("{{" "}}")
                | ("{{" expression_list "}}")
    
    expression_list : (expression ";" expression_list)
                    | (expression ";")
        
    expression : expression_var
               | expression_print
               | expression_for_lis
               | expression_for_var 

    
    expression_var : (variable_set ":=" string_expression)
                   | (variable_set ":=" string_list)
    
    expression_print : "print" string_expression
    
    expression_for_lis : "for" variable_set "in" string_list "do" expression_list "endfor"
    
    expression_for_var :  "for" variable_set "in" variable_get "do" expression_list "endfor"
                
    string_expression : string
                      | variable_get
                      | string_concat

    string_concat : string_expression "." string_expression
                          
    string_list : "(" string_list_interior ")"
    
    string_list_interior : string
                         | (string "," string_list_interior)
    
    variable_set : /[a-zA-Z_]\w*/   
    variable_get : /[a-zA-Z_]\w*/
    string : /'[^']+'/
    
    %ignore /[ \t\f\r\n]+/x
"""

calc_parser = Lark(calc_grammar, parser='lalr')
calc = calc_parser.parse


class TreeToDumbo(Transformer):

    def __init__(self, visit_tokens=True):
        super().__init__(visit_tokens)
        self.result = ""
        self.vars = {}
        self.list_strings = []
        self.list_expr = []

    def start(self, items):
        print(self.result)

    def program(self, items):
        pass

    def dumbo_block(self, items):
        return items

    def expression_list(self, items):
        res = self.list_expr
        self.list_expr = []
        if len(res) > 0:
            return res

    def expression(self, items):
        (val,) = items
        self.list_expr.append(val)

    def expression_print(self, items): # OK
        (val,) = items
        if val is not None:
            self.result += val

    def expression_for_lis(self, items):
        variable_set, list_string, expression_list = items


    def expression_for_var(self, items):
        variable_set, variable_get, expression_list = items
        for variable_set in variable_get:
            pass

    def expression_var(self, items): # OK Assign value to variable
        name, value = items
        self.vars[name] = value

    def string_expression(self, items): # OK
        (res,) = items
        return res

    def string_concat(self, items): # NOT TEST !!!
        (str1,), (str2,) = items
        return str1[1:-1] + str2[1:-1]

    def string_list(self, items): # OK
        res = self.list_strings
        self.list_strings = []
        return res

    def string_list_interior(self, items): # OK
        val = items[0]
        if val is not None:
            self.list_strings.append(items[0])

    def variable_get(self, item):
        (name,) = item
        if name in self.vars.keys():
            return self.vars[name]

    def variable_set(self, item):
        (name,) = item
        # print(f"variable_set ---> {name}")
        return name

    def string(self, item):     # OK
        (s,) = item
        res = s[1:-1]
        # print(f"string --> {res}")
        return res

    def txt(self, item):        # OK
        (res,) = item
        # print(f"txt --> {res}")
        self.result += res

    def get_vars(self, tree):
        print("******************************** DATA ****************************************")
        self.transform(tree)
        return self.vars

    def construct(self, tree, vars_):
        print("******************************** TEMPLATE ****************************************")
        self.vars = vars_
        self.transform(tree)


def test_lark(data, template):
    tree_data = calc(data)
    tree_template = calc(template)
    TreeToDumbo().construct(tree_template, TreeToDumbo().get_vars(tree_data))
