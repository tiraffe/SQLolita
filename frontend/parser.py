# coding=utf-8
# Created by Tian Yuanhao on 2016/3/25.

import ply.yacc as yacc
import lexer

# Get the token map.
tokens = lexer.tokens

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'LE', 'LE', 'GE', 'GT', 'EQ', 'NE'),  # Nonassociative operators
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', '-'),  # Unary minus operator
)


def p_start(p):
    """ start : command ';' """
    pass


def p_command(p):
    """ command : ddl
                | dml
                | utility
                | nothing """
    pass


def p_ddl(p):
    """ ddl : createtable
            | createindex
            | droptable
            | dropindex
            | showtables """
    pass


def p_dml(p):
    """ dml : query
            | insert
            | delete
            | update """
    pass


def p_utility(p):
    """ utility : load
                | exit
                | set
                | help
                | print """
    pass


def p_showtables(p):
    """ showtables : SHOW TABLES """
    pass


def p_createtable(p):
    """ createtable : CREATE TABLE ID '(' non_mattrtype_list ')' """
    pass


def p_createindex(p):
    """ createindex : CREATE INDEX ID '(' ID ')' """
    pass


def p_droptable(p):
    """ droptable : DROP TABLE ID """
    pass


def p_dropindex(p):
    """ dropindex : DROP INDEX ID '(' ID ')' """
    pass


def p_load(p):
    """ load : LOAD ID '(' STRING ')' """
    pass


def p_set(p):
    """ set : SET ID EQ STRING
            | SET ID EQ expr """
    pass


def p_help(p):
    """ help : HELP oprelname """
    pass


def p_print(p):
    """ print : PRINT ID """
    pass


def p_exit(p):
    """ exit : EXIT """
    pass


def p_query(p):
    """ query : SELECT non_mselect_clause FROM non_mrelation_list opwhere_clause """
    pass


def p_insert(p):
    """ insert : INSERT INTO ID VALUES inservalue_list """
    pass


def p_inservalue_list(p):
    """ inservalue_list : '(' non_mvalue_list ')' ',' inservalue_list
                        | '(' non_mvalue_list ')' """
    pass


def p_delete(p):
    """ delete : DELETE FROM ID opwhere_clause """
    pass


def p_update(p):
    """ update : UPDATE ID SET relattr EQ relattr_or_value opwhere_clause """
    pass


def p_non_mattrtype_list(p):
    """ non_mattrtype_list : attrtype ',' non_mattrtype_list
                           | attrtype """
    pass


def p_attrtype(p):
    """ attrtype : ID type
                 | ID type '(' INT ')'
                 | PRIMARY KEY '(' ID ')' """
    pass


def p_type(p):
    """ type : INT
             | CHAR """
    pass


def p_non_mselect_clause(p):
    """ non_mselect_clause : non_mrelattr_list
                           | '*' """
    pass


def p_non_mrelattr_list(p):
    """ non_mrelattr_list : relattr ',' non_mrelattr_list
                          | relattr """
    pass


def p_relattr(p):
    """ relattr : ID '.' ID
                | ID """
    pass


def p_non_mrelation_list(p):
    """ non_mrelation_list : relation ',' non_mrelation_list
                           | relation """
    pass


def p_relation(p):
    """ relation : ID """
    pass


def p_opwhere_clause(p):
    """ opwhere_clause : WHERE non_mcond_list
                       | nothing """
    pass


def p_non_mcond_list(p):
    """ non_mcond_list : condition AND non_mcond_list
                       | condition OR  non_mcond_list
                       | condition """
    pass


def p_condition(p):
    """ condition : relattr op relattr_or_value
                  | relattr IS NULL
                  | relattr IS NOT NULL """
    pass


def p_relattr_or_value(p):
    """ relattr_or_value : relattr
                         | value """
    pass


def p_non_mvalue_list(p):
    """ non_mvalue_list : value ',' non_mvalue_list
                        | value
                        | null_value ',' non_mvalue_list
                        | null_value """
    pass


def p_value(p):
    """ value : STRING
              | NUMBER """
    pass


def p_null_value(p):
    """ null_value : NULL """
    pass


def p_oprelname(p):
    """ oprelname : ID
                  | nothing """
    pass


def p_op(p):
    """ op : LT
           | LE
           | GT
           | GE
           | EQ
           | NE """
    pass


def p_expr(p):
    """ expr : expr '+' expr
             | expr '-' expr
             | expr '*' expr
             | expr '/' expr
             | expr AND expr
             | expr OR  expr
             | expr op  expr
             | '(' expr ')'
             | value
             | ID """
    pass


def p_nothing(p):
    """ nothing : """
    pass


# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"


# Build the parser
from lexer import lexer as lex

parser = yacc.yacc()

while True:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s, lexer=lex)
    print result
