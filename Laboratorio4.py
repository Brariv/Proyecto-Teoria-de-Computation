from graphviz import *

def txtreader(filename):
    while True:
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
            break
        except FileNotFoundError:
            print(f"File not found: {filename}")
            filename = input("Enter the path to the text file: ")
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            filename = input("Enter the path to the text file: ")
    return [line.strip() for line in lines]

def formatRegEx(regex):
    alloperators = ['|', '?', '+', '*', '^', ')']
    binaryoperators = ['|', '^', '(']
    res = ""

    for i in range(0, len(regex)):
        c1 = regex[i]

        if c1 == '\\' and i + 1 < len(regex):
            res += c1 + regex[i + 1]
            i += 1
            continue

        res += c1
        
        if (i + 1 < len(regex)):
            c2 = regex[i + 1]

            if c2 == '\\' and i + 2 < len(regex):
                c2 = regex[i + 2]

            if c1 != '(' and c2 != ')' and c2 not in alloperators and c1 not in binaryoperators:
                res += '∘'
    return res

def infixToPostfix(regex):
    postfix= ""
    stack = []
    regex = regex.replace(' ', '')
    formattedRegEx = formatRegEx(regex)
    print(f"Original regex: {regex}")
    print(f"Formatted regex before expansion: {formattedRegEx}")
    formattedRegEx = expand_regex(formattedRegEx)

    Precedence = { '(': 1, '|': 2, '∘': 3, '?': 4, '+': 4, '*': 4, '^': 5 }

    print (f"Formatted regex: {formattedRegEx}")

    for i in range(len(formattedRegEx)):
        if formattedRegEx[i] == '\\' and i + 1 < len(formattedRegEx):
            postfix += formattedRegEx[i]
            postfix += formattedRegEx[i + 1]
            print(f"Escaped character: {formattedRegEx[i + 1]}")
            print(f"Actual Output: {postfix} | Actual Stack: {stack}")
            i += 1
            continue

        char = formattedRegEx[i]

        if char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()
        elif char not in Precedence:
            postfix += char

        else:
            while (len(stack)):
                peekedChar = stack[-1]
                peekedCharPrecedence = Precedence[peekedChar]
                currentCharPrecedence = Precedence[char]
                if peekedCharPrecedence >= currentCharPrecedence:
                    postfix += stack.pop()
                else:
                    break
            stack.append(char)
            print(f"Operator {char} pushed to stack")
            print(f"Actual Output: {postfix} | Actual Stack: {stack}")

    while (len(stack) > 0):
        postfix += stack.pop()
        print(f"Actual Output: {postfix} | Actual Stack: {stack}")

    print()
    #postfix = postfix.replace('∘', '')
    return postfix

def expand_regex(regex):
    result = ""
    i = 0
    while i < len(regex):
        c = regex[i]

        if c == '\\':
            result += c + regex[i + 1]
            i += 2
            continue

        if c == '+':
            prev = result[-1]
            if prev == ')':
                # Encontrar el grupo que termina antes de +
                j = len(result) - 2
                balance = 1
                while j >= 0:
                    if result[j] == ')':
                        balance += 1
                    elif result[j] == '(':
                        balance -= 1
                    if balance == 0:
                        break
                    j -= 1
                group = result[j:]
                result += '∘' + group + '*'
            else:
                result = result[:-1] + prev + '∘' + prev + '*'
        elif c == '?':
            prev = result[-1]
            if prev == ')':
                # Encontrar el grupo que termina antes de ?
                j = len(result) - 2
                balance = 1
                while j >= 0:
                    if result[j] == ')':
                        balance += 1
                    elif result[j] == '(':
                        balance -= 1
                    if balance == 0:
                        break
                    j -= 1
                group = result[j:]
                result = result[:j] + '(' + group + '|ε)'
            else:
                result = result[:-1] + '(' + prev + '|ε)'
        else:
            result += c
        i += 1

    return result

def AST(postfix):
    stack = []
    binary_operators = ['|', '^']

    for i in range(len(postfix)):
        c = postfix[i]

        if c == '\\' and i + 1 < len(postfix):
            stack.append(c + postfix[i + 1])
            i += 1
            continue

        if c == '∘':
            if len(stack) >= 2:
                right = stack.pop()
                left = stack.pop()
                if isinstance(right, str):
                    stack.append((right, left))
                else:
                    stack.append((c, left, right))
            elif len(stack) == 1:
                operand = stack.pop()
                stack.append((operand))
        elif c  in binary_operators:
            right = stack.pop()
            left = stack.pop()
            stack.append((c, left, right))
        elif c == '*':
            operand = stack.pop()
            stack.append((c, operand))
        else:
            stack.append(c)

    return stack[-1] if stack else None

def sintax_tree(node, graph=None, parent=None):
    if graph is None:
        graph = Digraph()

    if parent is None:
        # Add the root node without an edge
        if isinstance(node, tuple):
            if len(node) == 2:  # Unary operator
                operator, operand = node
                graph.node(str(id(node)), label=operator)
                sintax_tree(operand, graph, node)
            elif len(node) == 3:  # Binary operator
                operator, left, right = node
                graph.node(str(id(node)), label=operator)
                sintax_tree(left, graph, node)
                sintax_tree(right, graph, node)
        else:
            graph.node(str(id(node)), label=node)
        return graph

    if isinstance(node, tuple):
        if len(node) == 2:  # Unary operator
            operator, operand = node
            graph.node(str(id(node)), label=operator)
            graph.edge(str(id(parent)), str(id(node)))
            sintax_tree(operand, graph, node)
        elif len(node) == 3:  # Binary operator
            operator, left, right = node
            graph.node(str(id(node)), label=operator)
            graph.edge(str(id(parent)), str(id(node)))
            sintax_tree(left, graph, node)
            sintax_tree(right, graph, node)
    else:
        graph.node(str(id(node)), label=node)
        graph.edge(str(id(parent)), str(id(node)))

    return graph

def main():
    filename = input("Enter the path to the text file: ")
    lines = txtreader(filename) 

    for line in lines:
        print(f"Processing line: {line}")
        print("-" * 100)
        postfix = infixToPostfix(line)
        print("-" * 100)
        print(f"Postfix notation: {postfix}")
        print("=" * 100 + "\n")
        ast = AST(postfix)
        print(f"AST: {ast}")
        sintax_tree_graph = sintax_tree(ast)
        sintax_tree_graph.render(f'sintax_tree_{lines.index(line) + 1}', format='png', cleanup=True)
        print("=" * 100 + "\n")

main()