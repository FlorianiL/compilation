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
        
    expression : expression_print
               | expression_for_lis
               | expression_for_var 
               | expression_var
    
    expression_print : "print" string_expression
    
    expression_for_lis : "for" VARIABLE "in" string_list "do" expression_list "endfor"
    
    expression_for_var :  "for" VARIABLE "in" VARIABLE "do" expression_list "endfor"
    
    expression_var : (VARIABLE ":=" string_expression)
                   | (VARIABLE ":=" string_list)
                
    string_expression : STRING
                      | VARIABLE
                      | (string_expression "." string_expression)
                          
    string_list : "(" string_list_interior ")"
    
    string_list_interior : STRING
                         | (STRING "," string_list_interior)
                                 
    VARIABLE : /[a-zA-Z_]\w*/
    STRING : /'[^']+'/
    
    %ignore /[ \t\f\r\n]+/x
"""

calc_parser = Lark(calc_grammar, parser='lalr')
calc = calc_parser.parse


class MyTransformer(Transformer):
    def program(self, items):
        pass

    def dumbo_block(self, items):
        pass

    def expression_list(self, items):
        pass

    def expression(self, items):
        pass

    def expression_print(self, items):
        pass

    def expression_for_lis(self, items):
        pass

    def expression_for_var(self, items):
        pass

    def expression_var(self, items):
        pass

    def string_expression(self, items):
        pass

    def string_list(self, items):
        pass

    def string_list_interior(self, items):
        pass


def test_lark(data, template):
    tree_data = calc(data)
    tree_template = calc(template)
    MyTransformer().transform(tree_data)
