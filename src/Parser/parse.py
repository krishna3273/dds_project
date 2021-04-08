import sqlparse
from sqlparse.tokens import Keyword, Whitespace, DML, DDL
from sqlparse.sql import Identifier, Token, IdentifierList, Statement
import moz_sql_parser
import boolean
import expression

from tree import *

class Parser():

    def __init__(self, config, schema):
        self.config = config
        self.alias_tables = {}
        self.schema = schema

    def parse(self, raw):
        statement = sqlparse.split(raw)[0]
        parsed = sqlparse.parse(statement)[0]
        self.parsed = parsed

        self.query_type = Statement(parsed.tokens).get_type()
        if(parsed.tokens[0].ttype == DML):
            self.query_type = "SELECT"
        else:
            self.query_type = "INSERT"

        self.columns = self.get_column_names()
        self.tables = self.extract_tables(parsed)
        if(self.query_type == "SELECT"):
            self.where = parsed[-1]

        self.expr_dict = {}
        self.get_tree()

    def get_column_names(self):
        ch_list = False
        stmt = None
        for tok in self.parsed.tokens:
            if(tok.ttype != Whitespace and tok.ttype != DML):
                stmt = tok.value
                break
        columns = stmt.split(", ")
        return columns

    def normalize(self, where):
        booleans = ['NOT', 'OR', 'AND']
        bool_ops = ['~', '|', '&']
        parenthesis = ['(', ')']
        expressions = []
        temp = ""

        # Extract expressions
        for token in where.flatten():

            tok = str(token)
            if(tok == " " or tok == ";" or tok.upper() == "WHERE"):
                continue
            if((tok not in booleans) and (tok not in parenthesis)):
                temp += tok
            else:
                if(temp not in expressions and temp != "" and temp.upper() != "WHERE"):
                    expressions.append(temp)
                temp = ""
        if (temp not in expressions and temp != "" and temp.upper() != "WHERE"):
            expressions.append(temp)
        temp = ""
        print("expr ", expressions)
        #Convert statement to boolean statement with expression variables
        bool_expr = ""
        vari = "x_"
        for token in where.flatten():
            tok = str(token)
            if(tok == " " or tok == ";" or tok.upper() == "WHERE"):
                continue
            if((tok not in booleans) and (tok not in parenthesis)):
                temp += tok
            else:
                if(temp != "" and temp.upper() != 'WHERE'):
                    indi = expressions.index(temp)
                    bool_expr += vari + str(indi)
                    self.expr_dict[bool_expr] = expressions[indi]
                if(tok in booleans):
                    tok = bool_ops[booleans.index(tok)]
                bool_expr += tok
                temp = ""
        if (temp != "" and temp.upper() != 'WHERE'):
            bool_expr += vari + str(expressions.index(temp))
        print("boolexpr ", bool_expr)
        #Evaluate boolean expression
        algebra = boolean.BooleanAlgebra()
        normalized = str(algebra.normalize(algebra.parse(bool_expr), algebra.AND))
        temp = ""
        fin_string = ""
        for charac in normalized:
            tok = charac
            if(tok == " " or tok == ";" or tok.upper() == "WHERE"):
                continue
            if((tok not in bool_ops) and (tok not in parenthesis)):
                temp += tok
            else:
                if(temp != "" and temp.upper() != 'WHERE'):
                    fin_string += expressions[int(temp.split("_")[-1])]
                if(tok in bool_ops):
                    tok = booleans[bool_ops.index(tok)]
                fin_string += " " + tok + " "
                temp = ""
        if (temp != "" and temp.upper() != 'WHERE'):
            fin_string += expressions[int(temp.split("_")[-1])]
        print("normal ", normalized)
        return normalized, expressions

    def extract_tables(self, parsed):
        from_seen = False
        lot = None
        tables = []
        for item in parsed.tokens:
            if from_seen:
                if(isinstance(item, sqlparse.sql.IdentifierList)):
                    lot = item
                    break
            elif item.ttype is Keyword and item.value.upper() == 'FROM':
                from_seen = True
        for tname in lot:
            if(isinstance(tname, sqlparse.sql.Identifier)):
                tables.append(tname.get_name())
                self.alias_tables[tname.get_alias()] = tname.get_real_name()

        return tables

    def get_tree(self):
        normalized, expressions = self.normalize(self.where)
        tree = Tree(self.get_column_names(), self.tables, normalized, expressions, self.schema)
        tree.print_tree(tree.root_node)
        tree.apply_rules(tree.root_node)




