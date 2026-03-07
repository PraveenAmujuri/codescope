def analyze_treesitter(tree, lang_obj):

    root = tree.root_node

    stats = {
        "loop_depth": 0,
        "functions": [],
        "recursive_functions": [],
        "heatmap": [],
        "call_graph": [],
        "flow_nodes": [],
        "flow_edges": [],
    }

    behavior = {
        "recursive_call": False,
        "log_loop": False
    }

    loop_types = {
        "for_statement",
        "while_statement",
        "do_statement",
        "range_based_for_statement"
    }

    func_types = {
        "function_definition",
        "function_declaration",
        "method_declaration"
    }

    action_types = {
        "expression_statement",
        "assignment_expression",
        "declaration",
        "return_statement"
    }

    # ------------------------------------------------
    # Graph helpers
    # ------------------------------------------------

    def add_node(node,label,ntype="process"):

        node_id=f"{node.type}_{node.start_point[0]}_{node.start_point[1]}"

        stats["flow_nodes"].append({
            "id":node_id,
            "type":ntype,
            "data":{"label":label}
        })

        return node_id


    def add_edge(src,dst,label=""):

        stats["flow_edges"].append({
            "id":f"e-{src}-{dst}",
            "source":src,
            "target":dst,
            "label":label
        })


    # ------------------------------------------------
    # Behavior detection
    # ------------------------------------------------

    def detect_behavior(node,current_func):

        node_text=node.text.decode("utf8").lower()

        # ---------------------------
        # recursion detection
        # ---------------------------
        if node.type == "call_expression":

            call_name = None

            for child in node.children:
                if "identifier" in child.type:
                    call_name = child.text.decode("utf8").split("::")[-1].lower()
                    break
            if call_name:

                stats["call_graph"].append({
                    "source": current_func,
                    "target": call_name
                })

                if call_name == current_func:

                    behavior["recursive_call"] = True

                    if current_func not in stats["recursive_functions"]:
                        stats["recursive_functions"].append(current_func)

        # ---------------------------
        # logarithmic loop detection
        # ---------------------------
        if node.type == "assignment_expression":

            text=node_text.replace(" ","")

            if "/=2" in text or "*=2" in text or ">>=1" in text:
                behavior["log_loop"]=True


    # ------------------------------------------------
    # AST walk
    # ------------------------------------------------

    def walk(node,prev_node=None,current_func="Global",depth=0):

        detect_behavior(node,current_func)

        node_text=node.text.decode("utf8")

        # FUNCTION
        if node.type in func_types:

            name_node = node.child_by_field_name('declarator')
            name = "function"

            if name_node:

                for c in name_node.children:
                    if "identifier" in c.type:
                        name = c.text.decode("utf8").lower()
                        break

                if name == "function":
                    name = name_node.text.decode("utf8").split("(")[0].strip().lower()

            stats["functions"].append(name)

            start_id=add_node(node,f"Start: {name}","start")

            if prev_node:
                add_edge(prev_node,start_id)

            prev_node=start_id
            current_func=name


        # LOOP
        # LOOP
        if node.type in loop_types:

            depth += 1
            stats["loop_depth"] = max(stats["loop_depth"], depth)

            cond = node.child_by_field_name("condition")
            update = node.child_by_field_name("update")

            if update:
                update_text = update.text.decode("utf8").replace(" ","")

                if "*=2" in update_text or "/=2" in update_text or ">>=1" in update_text:
                    behavior["log_loop"] = True

            label = cond.text.decode("utf8") if cond else node.type

            # create loop node FIRST
            loop_id = add_node(
                node,
                f"{node.type.replace('_statement','')} ({label})",
                "decision"
            )

            if prev_node:
                add_edge(prev_node, loop_id)

            stats["heatmap"].append({
                "line": node.start_point[0] + 1,
                "severity": "medium",
                "message": "Loop detected"
            })

            # detect loop body
            body = node.child_by_field_name("body")

            if body is None:
                for child in node.children:
                    if "statement" in child.type or child.type == "compound_statement":
                        body = child
                        break

            body_last = [loop_id]

            if body:
                new_exits = []

                for e in body_last:
                    for child in body.children:

                        result = walk(child, e, current_func, depth)

                        if isinstance(result, list):
                            new_exits.extend(result)
                        else:
                            new_exits.append(result)

                body_last = new_exits

            # loop back edges
            for e in body_last:
                add_edge(e, loop_id, "loop")

            return [loop_id]

        # IF
        if node.type=="if_statement":

            cond=node.child_by_field_name("condition")
            label=cond.text.decode("utf8") if cond else "if"

            if_id=add_node(node,f"if ({label})","decision")

            if prev_node:
                add_edge(prev_node,if_id)

            exits=[]

            consequence=node.child_by_field_name("consequence")

            if consequence:
                yes_last=if_id
                for child in consequence.children:
                    yes_last=walk(child,yes_last,current_func,depth)

                if isinstance(yes_last,list):
                    exits.extend(yes_last)
                else:
                    exits.append(yes_last)

            alt=node.child_by_field_name("alternative")

            if alt:
                no_last=if_id
                for child in alt.children:
                    no_last=walk(child,no_last,current_func,depth)

                if isinstance(no_last,list):
                    exits.extend(no_last)
                else:
                    exits.append(no_last)
            else:
                exits.append(if_id)

            return exits


        # ACTION
        if node.type in action_types:

            label=node_text.split(";")[0]

            if node.type=="return_statement":

                nid=add_node(node,label,"end")

                if prev_node:
                    add_edge(prev_node,nid)

                return None

            nid=add_node(node,label)

            if prev_node:
                add_edge(prev_node,nid)

            return nid
        # DEFAULT WALK (important)
        last = prev_node

        for child in node.children:
            result = walk(child, last, current_func, depth)

            if isinstance(result, list):
                if result:
                    last = result[-1]
            else:
                last = result

        return last




    walk(root)

    depth=stats["loop_depth"]

    # ------------------------------------------------
    # Complexity estimation
    # ------------------------------------------------

    if behavior["log_loop"]:
        complexity="O(log n)"

    elif behavior["recursive_call"] and depth==0:
        complexity="O(n)"

    else:
        complexity=(
            "O(1)" if depth==0 else
            "O(n)" if depth==1 else
            f"O(n^{depth})"
        )


    return {
        "loop_depth":depth,
        "estimated_complexity":complexity,
        "functions":stats["functions"],
        "recursive_functions":stats["recursive_functions"],
        "heatmap":stats["heatmap"],
        "flow_data":{
            "nodes":stats["flow_nodes"],
            "edges":stats["flow_edges"]
        }
    }