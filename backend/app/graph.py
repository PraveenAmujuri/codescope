import ast


class FlowBuilder:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.counter = 0

    def new_id(self, prefix):
        self.counter += 1
        return f"{prefix}_{self.counter}"

    def add_node(self, label, n_type):
        node_id = self.new_id(n_type)
        self.nodes.append({
            "id": node_id,
            "type": n_type,
            "data": {"label": label}
        })
        return node_id

    def add_edge(self, src, dst, label=""):
        self.edges.append({
            "id": f"e-{src}-{dst}",
            "source": src,
            "target": dst,
            "label": label
        })


def generate_python_flow(tree):

    builder = FlowBuilder()

    def walk_block(statements, incoming):

        current_exits = incoming

        for stmt in statements:
            current_exits = walk(stmt, current_exits)

        return current_exits


    def connect_all(src_list, target):
        for s in src_list:
            builder.add_edge(s, target)


    def walk(node, incoming):

        # ---------------- FUNCTION ----------------
        if isinstance(node, ast.FunctionDef):

            start = builder.add_node(f"Start: {node.name}", "start")

            connect_all(incoming, start)

            exits = walk_block(node.body, [start])

            return exits


        # ---------------- IF ----------------
        elif isinstance(node, ast.If):

            cond = ast.unparse(node.test)

            decision = builder.add_node(f"if {cond}", "decision")

            connect_all(incoming, decision)

            # True branch
            true_exits = walk_block(node.body, [decision])

            # False branch
            if node.orelse:
                false_exits = walk_block(node.orelse, [decision])
            else:
                false_exits = [decision]

            return true_exits + false_exits


        # ---------------- WHILE ----------------
        elif isinstance(node, ast.While):

            cond = ast.unparse(node.test)

            decision = builder.add_node(f"while {cond}", "decision")

            connect_all(incoming, decision)

            body_exits = walk_block(node.body, [decision])

            # loop back
            for exit_node in body_exits:
                builder.add_edge(exit_node, decision, "loop")

            return [decision]


        # ---------------- FOR ----------------
        elif isinstance(node, ast.For):

            label = f"for {ast.unparse(node.target)} in {ast.unparse(node.iter)}"

            decision = builder.add_node(label, "decision")

            connect_all(incoming, decision)

            body_exits = walk_block(node.body, [decision])

            for exit_node in body_exits:
                builder.add_edge(exit_node, decision, "loop")

            return [decision]


        # ---------------- RETURN ----------------
        elif isinstance(node, ast.Return):

            label = "return"

            n = builder.add_node(label, "end")

            connect_all(incoming, n)

            return []


        # ---------------- CALL ----------------
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):

            label = ast.unparse(node.value)

            n = builder.add_node(label, "process")

            connect_all(incoming, n)

            return [n]


        # ---------------- ASSIGN ----------------
        elif isinstance(node, ast.Assign):

            label = ast.unparse(node)

            n = builder.add_node(label, "process")

            connect_all(incoming, n)

            return [n]


        else:
            return incoming


    incoming = []

    for stmt in tree.body:
        incoming = walk(stmt, incoming)

    return {
        "nodes": builder.nodes,
        "edges": builder.edges
    }


def format_treesitter_flow(flow_data):
    return flow_data