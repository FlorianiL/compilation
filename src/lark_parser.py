from lark import Lark, Transformer, v_args

calc_grammar = """
    start : program
    
    program : program_t | program_b | program_tp | program_bp
    
    program_t : txt
    
    program_b : dumbo_bloc
    
    program_tp : txt program
    
    program_bp : dumbo_bloc program
    
    txt : expression_list_rec
        | expression
    
    dumbo_bloc : "{{" expression_list_rec "}}"
    
    expression_list_rec : expression ";" expression_list_rec
    
    expression_list_end : expression ";"
    
    expression : expression_print
               | expression_for_list
               | expression_for_var 
               | expression_var
    
    expression_print : "print" string_expression
    
    expression_for_list : "for" VARIABLE "in" string_list "do" expression_list_rec "endfor"
    
    expression_for_var :  "for" VARIABLE "in" VARIABLE "do" expression_list_rec "endfor"
    
    expression_var : VARIABLE ":=" string_expression
                   | VARIABLE ":=" string_list 
                
    string_expression : string
                      | VARIABLE
                      | string_expression "." string_expression
                          
    string_list : "(" string_list_interior ")"
    
    string_list_interior : string
                         | string "," string_list_interior
    
    string : "'"/\w+/"'"
                             
    VARIABLE : /[a-zA-Z_]\w*/
            
    %ignore /[ \t\f\r]+/

"""
calc_parser = Lark(calc_grammar, parser='lalr')
calc = calc_parser.parse


def test_lark(data, template):
    print(calc(data))
