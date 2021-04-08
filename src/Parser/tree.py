import re

class Node():
    def __init__(self, type):
        self.type = type
        self.metadata = {}
        self.children = []
        self.parent = None

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def add_child_at_first(self, node):
        self.children.insert(0, node)
        node.parent = self




class Tree():
    def __init__(self, column_names, tables, expr, conds, schema):
        self.column_names = column_names
        self.tables = tables
        self.expr = expr
        self.conds = conds
        self.schema = schema
        self.root_node = self.build_initial_tree()

    def print_tree(self, node):

        print("< ", node.type, " ", node.metadata, " >")
        for child in node.children:
            self.print_tree(child)


    def build_initial_tree(self):

        ## Build cartesian product of tables
        node1 = Node("Table")
        node1.metadata["name"] = self.tables[0]
        node2 = Node("Table")
        node2.metadata["name"] = self.tables[1]

        node = self._cartesian_merge(node1, node2)
        for i in range(2, len(self.tables)):
            node_temp = Node("Table")
            node_temp.metadata["name"] = self.tables[i]
            node = self._cartesian_merge(node, node_temp)

        select_node = Node("Select")
        select_node.metadata["expr"] = self.expr
        select_node.add_child(node)
        project_node = Node("Project")
        project_node.metadata["columns"] = self.column_names
        project_node.add_child(select_node)
        return project_node

    def apply_rules(self, node):

        # Rule 1: Move down SELECT operations
        cond_exprns = self.expr.split("&")
        for exprsn in cond_exprns:
            print("Moving down ", exprsn)
            self._move_down(exprsn, node)
        child_sel_node = self.root_node.children[0]
        temp_node = child_sel_node.children[0]
        self.root_node.children.remove(child_sel_node)
        self.root_node.add_child(temp_node)

        # Rule 2: combine SELECT condition and CARTESIAN PRODUCT to JOIN
        self._dfs_join(self.root_node)

        #Rule 3: move down project operations
        self._propogate_proj(self.root_node)

        self.print_tree(self.root_node)

    def gen_fragment_tree(self):

        # Rule 1: split relations into fragments
        self._split_relation_dfs(self.root_node)

    def _split_relation_dfs(self, node):
        if (node.type == "Table"):
            union_node = Node("Union")
            frags = self._get_frags(node.metadata['name'])
            for frag in frags:
                frag_node = Node(frag["relation"] + frag["Fragment_id"])
                frag_node.metadata = frag
                union_node.add_child(frag_node)
            parent_node = node.parent
            parent_node.children.remove(node)
            parent_node.add_child(union_node)
            return
        for child in node.children:
            self._split_relation_dfs(child)

    def _get_frags(self, table):
        pass

    def _propogate_proj(self, node):
        if(node.type == 'Project' and node.children[0].type == 'Join'):
            child = node.children[0]
            pnode1 = Node("Project")
            pnode2 = Node("Project")
            ind_expr = int(child.metadata['expr'].split("_")[-1])
            left, _, right = self._get_parse_expr(self.conds[ind_expr])
            cols1 = []
            cols2 = []
            for col in node.metadata["columns"]:
                if(col.find(".")):
                    tabl = col.split(".")[0]
                else:
                    #tabl = find_table_from_col(col)
                    tabl = None
                if tabl in child.metadata["left"]:
                    cols1.append(col)
                else:
                    cols2.append(col)

            tab = left.split(".")[0]
            if(tab in child.metadata["left"]):
                cols1.append(left)
                cols2.append(right)
            else:
                cols1.append(right)
                cols2.append(left)

            pnode1.metadata["columns"] = cols1
            pnode2.metadata["columns"] = cols2

            gc1 = child.children[0]
            child.children.remove(gc1)
            child.add_child_at_first(pnode1)
            pnode1.add_child(gc1)

            gc2 = child.children[1]
            child.children.remove(gc2)
            child.add_child(pnode2)
            pnode2.add_child(gc2)

            self._propogate_proj(pnode1)
            self._propogate_proj(pnode2)
        return

    def _get_parse_expr(self, cond):
        ops = ["<=", ">=", "<", ">", "!=", "="]
        res = []
        res_op = None
        for op in ops:
            if(cond.find(op) != -1):
                res = cond.split(op)
                print(res, op)
                res_op = op
                break
        return res[0], res_op, res[1]

    def _dfs_join(self, node):
        for child in node.children:
            if(node.type == "Select"):
                if(len(node.children) != 1):
                    print("Error: Select Node has multiple children")
                    return
                if(child.type == "CartesianProduct"):
                    parent_node = node.parent
                    join_node = Node("Join")
                    join_node.metadata["expr"] = node.metadata["expr"]
                    join_node.metadata["left"] = child.metadata["left"]
                    join_node.metadata["right"] = child.metadata["right"]
                    ind = parent_node.children.index(node)
                    parent_node.children.remove(node)
                    if(ind == 1):
                        parent_node.add_child(join_node)
                    else:
                        parent_node.add_child_at_first(join_node)
                    print("--------")
                    print(node.type, " ", node.metadata)
                    for grandchild in child.children:
                        print(grandchild.type, " ", grandchild.metadata)
                        join_node.add_child(grandchild)
                    print("--------")
            self._dfs_join(child)

    def _move_down(self, exprsn, node):
        tables = self._get_tables(exprsn)
        # print("Expression: ", exprsn, "Tables: ", tables, "nod: ", node.metadata)
        if(node.type == "CartesianProduct"):
            # print(tables, " ", node.metadata["left"], " ", node.metadata["right"], " ", bool(set(tables) & set(node.metadata["left"])), " ", bool(set(tables) & set(node.metadata["right"])))
            if (bool(set(tables) & set(node.metadata["left"])) and bool(set(tables) & set(node.metadata["right"]))):
                select_node = Node("Select")
                select_node.metadata["expr"] = exprsn
                parent_node = node.parent
                ind = parent_node.children.index(node)
                parent_node.children.remove(node)
                if(ind == 1):
                    parent_node.add_child(select_node)
                else:
                    parent_node.add_child_at_first(select_node)
                select_node.add_child(node)
                return
            elif(bool(set(tables) & set(node.metadata["left"]))):
                self._move_down(exprsn, node.children[0])
            elif(bool(set(tables) & set(node.metadata["right"]))):
                self._move_down(exprsn, node.children[1])
            return

        if(node.type == "Table"):
            if(len(tables) != 1):
                print("Error")
            select_node = Node("Select")
            select_node.metadata["expr"] = exprsn
            parent_node = node.parent
            ind = parent_node.children.index(node)
            parent_node.children.remove(node)
            if(ind == 1):
                parent_node.add_child(select_node)
            else:
                parent_node.add_child_at_first(select_node)
            select_node.add_child(node)
            return
        else:
            for child in node.children:
                self._move_down(exprsn, child)
        return
    def _get_tables(self, expn):
        bool_exprs = re.findall(r'x_.', expn)
        ops = ["<=", ">=", "<", ">", "!=", "="]
        tables = []
        reg = r'^-?\d+(\.\d{1,2})?$'
        for be in bool_exprs:
            ind = int(be.split("_")[-1])
            cond = self.conds[ind]
            spl_arr = None
            for op in ops:
                if(cond.find(op) != -1):
                    spl_arr = cond.split(op)
                    break
            for con in spl_arr:
                if((con[0] == "'" and con[-1] == "'") or re.match(reg, con)):
                    continue
                else:
                    tables.append(con.split(".")[0])
                    """
                        tables.append(self.schema["column"][con.split["."][-1]]) 
                    """
        return tables

    def _cartesian_merge(self, node1, node2):
        cartesian_node = Node("CartesianProduct")
        cartesian_node.add_child(node1)
        cartesian_node.add_child(node2)
        cartesian_node.metadata["left"] = []
        cartesian_node.metadata["right"] = []

        if(node1.type == "Table"):
            cartesian_node.metadata["left"] = [node1.metadata["name"]]
        elif(node1.type == "CartesianProduct"):
            cartesian_node.metadata["left"] = node1.metadata["left"] + node1.metadata["right"]
        else:
            print("error: Node type")

        if (node2.type == "Table"):
            cartesian_node.metadata["right"] = [node2.metadata["name"]]
        elif (node2.type == "CartesianProduct"):
            cartesian_node.metadata["right"] = node2.metadata["left"] + node2.metadata["right"]
        else:
            print("error:Node type")

        return cartesian_node

