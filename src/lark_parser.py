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

    
    expression_var : (NAME_VAR ":=" string_expression)
                   | (NAME_VAR ":=" string_list)
    
    expression_print : "print" string_expression
    
    expression_for_lis : "for" NAME_VAR "in" string_list "do" expression_list "endfor"
    
    expression_for_var :  "for" NAME_VAR "in" var "do" expression_list "endfor"
                
    string_expression : string
                      | var
                      | string_concat

    string_concat : string_expression "." string_expression
                          
    string_list : "(" string_list_interior ")"
    
    string_list_interior : string
                         | (string "," string_list_interior)
    
    var : /[a-zA-Z_]\w*/   
    NAME_VAR : /[a-zA-Z_]\w*/
    string : /'[^']+'/
    
    %ignore /[ \t\f\r\n]+/x
"""

calc_parser = Lark(calc_grammar, parser='lalr')
calc = calc_parser.parse


class TreeToDumbo(Transformer):
    def __init__(self, visit_tokens=True):
        super().__init__(visit_tokens)
        self.vars = {}

    def transform(self, tree):
        super().transform(tree)
        print(self.vars)

    def program(self, items):
        print(items)

    def txt(self, items):
        print(items)

    def dumbo_block(self, items):
        print(items)

    def expression_list(self, items):
        print(f"expression_list --> {items}")

    def expression(self, items):
        print(f"expression --> {items}")

    def expression_var(self, items):
        name, value = items
        if type(value) == lark.tree.Tree:
            value = self.transform(value)
        self.vars[name] = value
        return value

    def expression_print(self, items):
        (value,) = items
        if type(value) == lark.tree.Tree:
            value = self.transform(value)
        print(f"print --> {value}")
        return print(value)

    def expression_for_lis(self, items):
        print(f"for_lis --> {items}")

    def expression_for_var(self, items):
        print(f"for_var --> {items}")

    def string_expression(self, items):
        print(items)

    def string_concat(self, items):
        (str1,), (str2,) = items
        return str1[1:-1] + str2[1:-1]

    def string_list(self, items):
        print(f"string_list ---> {items}")
        (val,) = items
        print(val)
        for item in items:
            print(type(item))
        return list(self.transform(items))

    def string_list_interior(self, items):
        print(f"string_list_interior ---> {items}")
        if len(items) > 1:
            value, rest = items
            print(rest)
        else:
            value = items
        print(f"string_list_interior ---> {value}")
        return value

    def var(self, item):
        (name,) = item
        print(f"name ---> {name}")
        return name

    def string(self, item):
        (s,) = item
        return s[1:-1]

def test_lark(data, template):
    tree_data = calc(data)
    tree_template = calc(template)
    print("************************ DATA **********************************")
    TreeToDumbo().transform(tree_data)
    print("************************ TEMPLATE **********************************")
    TreeToDumbo().transform(tree_template)
