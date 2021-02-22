import sqlparse
from sqlparse.tokens import Keyword
import moz_sql_parser
import boolean
import expression

from tree import *

class Parser():

    def __init__(self, config):
        self.config = config

    def parse(self, raw):
        statement = sqlparse.split(raw)[0]
        parsed = sqlparse.parse(statement)[0]
        self.parsed = parsed
        print(parsed.tokens)
        self.where = parsed[-1]
        self.expr_dict = {}
        self.get_tree()

    def perform_decomposition(self, parsed):
        where = parsed.tokens[-1]


    def normalize(self, where):
        booleans = ['NOT', 'OR', 'AND']
        bool_ops = ['~', '|', '&']
        parenthesis = ['(', ')']
        expressions = []
        temp = ""

        # Extract expressions
        for token in where.flatten():
            tok = str(token)
            if(tok == " "):
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
            if (tok == " "):
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
            if (tok == " "):
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
        return tables

    def get_tree(self):
        tables = self.extract_tables(self.parsed)
        leaf_nodes = []
        for table in tables:
            leaf_nodes.append(Node(table))

        ops = ['&', '|', '~']
        pars = ['(', ')']
        normalized, expressions = self.normalize(self.where)
        temp = ""

        # for tok in normalized:
        #     if(tok == " " or tok == ""):
        #         continue
        #     if(tok not in ops and tok not in pars):
        #         temp += tok
        #     else:
        #         if(temp[0] == '~'):
        #             expr = self.transform(self.expr_dict[temp[1:]])
        #         else:
        #             expr = self.expr_dict[temp]






