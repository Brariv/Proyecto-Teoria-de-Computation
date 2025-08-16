from graphviz import Digraph

# postfix to an ASt implementation (like you can do the nda parsing with the postfi,) 
def postfixToAst(postfix:str) -> str:

    # flatten ast
    ast:list  = []

    for i in range(len(postfix)):
        c = postfix[i]
        if c == '.':
            if len(ast) >= 2:

                right = ast.pop()
                left = ast.pop()
                ast.append((c, left, right))

            elif len(ast) == 1:
                operand = ast.pop()
                ast.append((operand))

        elif c  in ['|', '^']:

            right = ast.pop()
            left = ast.pop()

            ast.append((c, left, right))
        elif c == '*':

            operand = ast.pop()
            ast.append((c, operand))
        else:

            ast.append(c)

    print(ast)
    return ast[-1]


# This function the only porpuse it's to turn the AST from the postfix (which can be parse with te graphviz AST method)
def astToGraph(node: str, graph:Digraph | None = None, parent:tuple | None = None) -> Digraph:
    if graph is None:
        graph = Digraph() # for the base case

    if parent is None:
        # Add the root node without an edge
        if isinstance(node, tuple):
            if len(node) == 2:  # Unary operator (like the klean)
                operator, operand = node
                graph.node(str(id(node)), label=operator)
                astToGraph(operand, graph, node)
            elif len(node) == 3:  # Binary operator
                operator, left, right = node
                graph.node(str(id(node)), label=operator)
                astToGraph(left, graph, node)
                astToGraph(right, graph, node)
        else:
            graph.node(str(id(node)), label=node)
        return graph

    if isinstance(node, tuple):
        if len(node) == 2:  # Unary operator (like the klean)
            operator, operand = node
            graph.node(str(id(node)), label=operator)
            graph.edge(str(id(parent)), str(id(node)))
            astToGraph(operand, graph, node)
        elif len(node) == 3:  # Binary operator
            operator, left, right = node
            graph.node(str(id(node)), label=operator)
            graph.edge(str(id(parent)), str(id(node)))
            astToGraph(left, graph, node)
            astToGraph(right, graph, node)
    else:
        graph.node(str(id(node)), label=node)
        graph.edge(str(id(parent)), str(id(node)))

    return graph


