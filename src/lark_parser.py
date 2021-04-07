from lark import Lark

calc_grammar = """
    start : program
    
    program : txt
            | txt program
            | dumbo_block
            | dumbo_block program
    
    txt : /[ a-zA-Z0-9_;&<>"-.:,\n]+/x
    
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


def test_lark(data, template):
    print(calc(data))
