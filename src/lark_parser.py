import copy

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
        self.vars = {}
        self.temp = []

    def program(self, items):
        print(f"program --> {items}")
        return items

    def dumbo_block(self, items):
        print(f"dumbo_block --> {items}")
        return items

    def expression_list(self, items):
        print(f"expression_list --> {items}")
        return items

    def expression(self, items):
        print(f"expression --> {items}")
        return items

    def expression_var(self, items): # OK
        name, value = items
        self.vars[name] = value
        print(f"expression_var --> {name} {self.vars[name]}")

    def expression_print(self, items):
        print(f"expression_print --> {items}")
        return items

    def expression_for_lis(self, items):
        print(f"expression_for_lis --> {items}")
        return items

    def expression_for_var(self, items):
        print(f"expression_for_var --> {items}")
        return items

    def string_expression(self, items): # OK
        (res,) = items
        print(f"string_expression --> {res}")
        return res

    def string_concat(self, items): # NOT TEST !!!
        print(f"string_concat --> {items}")
        (str1,), (str2,) = items
        return str1[1:-1] + str2[1:-1]

    def string_list(self, items): # OK
        res = self.temp
        self.temp = []
        print(f"string_list ---> {res}")
        return res

    def string_list_interior(self, items): # OK
        self.temp.append(items[0])
        print(f"string_list_interior ---> {self.temp} ")

    def variable_get(self, item):
        (name,) = item
        print(f"variable_get ---> {name}")
        return name

    def variable_set(self, item):
        (name,) = item
        print(f"variable_set ---> {name}")
        return name

    def string(self, item):     # OK
        (s,) = item
        res = s[1:-1]
        print(f"string --> {res}")
        return res

    def txt(self, item):        # OK
        (res,) = item
        print(f"txt --> {res}")
        return res


def test_lark(data, template):
    tree_data = calc(data)
    tree_template = calc(template)
    print("************************ DATA **********************************")
    TreeToDumbo().transform(tree_data)
    # print("************************ TEMPLATE **********************************")
    # TreeToDumbo().transform(tree_template)
