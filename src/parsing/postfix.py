# this is a pretty big code snippet, but it does it's job
def _expandRegex(regex):
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



def _formatRegEx(regex):
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

    postfix = ""
    stack = []

    regex = regex.replace(' ', '') # removing any weird space that the bad formated regex can have

    formattedRegEx = _formatRegEx(regex)
    print(f"Original regex: {regex}")
    print(f"Formatted regex before expansion: {formattedRegEx}")
    formattedRegEx = _expandRegex(formattedRegEx)

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
    return postfix


