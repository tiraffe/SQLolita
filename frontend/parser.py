# coding=utf-8
# Created by Tian Yuanhao on 2016/3/25.
from string import upper

import ply.yacc as yacc
from nodes import *
import lexer

# Get the token map.
tokens = lexer.tokens

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'LE', 'LE', 'GE', 'GT', 'EQ', 'NE'),  # Nonassociative operators
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
            | showtables
            | alerttable
            | createuser
            | grantuser
            | revokeuser """
    pass


def p_dml(p):
    """ dml : query
            | insert
            | delete
            | update """
    pass


def p_utility(p):
    """ utility : exit
                | print """
    pass


def p_showtables(p):
    """ showtables : SHOW TABLES """
    pass


def p_createuser(p):
    """ createuser : CREATE USER ID PASSWORD STRING"""
    pass


def p_grantuser(p):
    """ grantuser : GRANT non_mrelation_list ON non_mrelation_list TO non_mrelation_list """
    pass


def p_revokeuser(p):
    """ revokeuser : REVOKE non_mrelation_list ON non_mrelation_list FROM non_mrelation_list """
    pass


def p_alerttable(p):
    """ alerttable : ALERT TABLE ID ADD ID type
                   | ALERT TABLE ID DROP non_mrelation_list """
    if upper(p[4]) == 'ADD':
        p[0] = AlertNode(p[3], 'ADD', (p[5], p[6]))
    else:
        p[0] = AlertNode(p[3], 'DROP', p[5])


def p_createtable(p):
    """ createtable : CREATE TABLE ID '(' non_mattrtype_list ')' """
    p[0] = CreateTableNode(p[3], p[5])


def p_createindex(p):
    """ createindex : CREATE INDEX ID '(' ID ')' """
    p[0] = CreateIndexNode(p[3], p[5])


def p_droptable(p):
    """ droptable : DROP TABLE ID """
    p[0] = DropTableNode(p[3])


def p_dropindex(p):
    """ dropindex : DROP INDEX ID '(' ID ')' """
    p[0] = DropIndexNode(p[3], p[5])


def p_print(p):
    """ print : PRINT ID """

    pass


def p_exit(p):
    """ exit : EXIT """
    pass


def p_query(p):
    """ query : SELECT non_mselect_clause FROM non_mrelation_list opwhere_clause """
    p[0] = QueryNode(p[2], p[4], p[5])


def p_insert(p):
    """ insert : INSERT INTO ID VALUES inservalue_list """
    p[0] = InsertNode(p[3], p[5])


def p_inservalue_list(p):
    """ inservalue_list : '(' non_mvalue_list ')' ',' inservalue_list
                        | '(' non_mvalue_list ')' """
    if len(p) > 4:
        p[0] = [p[2]] + p[5]
    else:
        p[0] = [p[2]]


def p_delete(p):
    """ delete : DELETE FROM ID opwhere_clause """
    p[0] = DeleteNode(p[3], p[4])


def p_update(p):
    """ update : UPDATE ID SET relattr EQ relattr_or_value opwhere_clause """
    p[0] = UpdateNode(p[2], [p[4], p[6]], p[7])


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
    """ non_mcond_list : non_mcond_list AND non_mcond_list
                       | non_mcond_list OR  non_mcond_list
                       | '(' non_mcond_list ')'
                       | condition """
    if(len(p) == 4): print p[2]
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
    if len(p) == 1:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_value_string(p):
    """ value : STRING """
    p[0] = Value('STRING', p[1])
    print(p[0])


def p_value_number(p):
    """ value : NUMBER """
    p[0] = Value('NUMBER', p[1])
    print(p[0])


def p_null_value(p):
    """ null_value : NULL """
    p[0] = Value('NULL', 0)


def p_op(p):
    """ op : LT
           | LE
           | GT
           | GE
           | EQ
           | NE """
    p[0] = p[1]


def p_nothing(p):
    """ nothing : """
    pass


# Error rule for syntax errors
def p_error(p):
    print "Syntax error at token '%s'(%s)" % (p.value, p.type)


# Build the parser
from lexer import lexer as lex

parser = yacc.yacc()

if __name__ == '__main__':
    while True:
        try:
            s = raw_input('Parser > ')
        except EOFError:
            break
        if not s: continue
        try:
            result = parser.parse(s, lexer=lex)
            print result
        except Exception, e:
            print(e)
