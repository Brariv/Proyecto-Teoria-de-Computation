
# Balances the parentheses given expression some expression
def _balanceExpression(expression_to_balance:str) -> str:
    j = len(expression_to_balance) - 2
    balance = 1
    while j >= 0:
        if expression_to_balance[j] == ')':
            balance += 1
        elif expression_to_balance[j] == '(':
            balance -= 1
        if balance == 0:
            break
        j -= 1

    return expression_to_balance[j:]

# this is a pretty big code snippet, but it does it's job
def _expandRegex(regex:str) -> str:

    result:str = str()

    i:int = 0

    while i < len(regex):
        c = regex[i]

        match c:
            case '\n':
                result += c + regex[i + 1]
                i += 2
                continue

            case '+':
                prev:str = result[-1]
                if prev == ')':
                    result += '.' + _balanceExpression(result) + '∗'
                else:
                    result = result[:-1] + prev + '.' + prev + '∗'
            case '?':
                prev:str = result[-1]
                if prev == ')':
                    # Same as the + but for the ?
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
                    result = result[:j] + '(' + _balanceExpression(result) + '|𝜀)'
                else:
                    result = result[:-1] + '(' + prev + '|𝜀)'
            case _:
                result += c

        i += 1

    return result



def _formatRegEx(regex):

    # this way of doing "static" declaraction I like, but not using the F***** []
    alloperators:list[str] = ['|', '?', '+', '∗', ')']
    binaryoperators:list[str] = ['|', '(']

    res:str = str()

    for i in range(0, len(regex)):
        c1:str = regex[i]

        if c1 == '\n' and i + 1 < len(regex):
            res += c1 + regex[i + 1]
            i += 1
            continue

        res += c1
        
        if (i + 1 < len(regex)):
            c2:str = regex[i + 1]

            if c2 == '\n' and i + 2 < len(regex):
                c2 = regex[i + 2]

            if c1 != '(' and c2 != ')' and c2 not in alloperators and c1 not in binaryoperators:
                res += '.'

    return res


def infixToPostfix(regex:str) -> str:

    postfix:str = str() # don't like to initialize strings with an empty one explictly
    stack:list[str] = list()

    regex = regex.replace(' ', '') # removing any weird space that the bad formated regex can have

    formattedRegEx = _formatRegEx(regex)

    formattedRegEx = _expandRegex(formattedRegEx)

    precedence:dict[str,int] = { 
        '(': 1, 
        '|': 2, 
        '.': 3, 
        '∗': 4, 
    }


    for i in range(len(formattedRegEx)):
        if formattedRegEx[i] == '\n' and i + 1 < len(formattedRegEx):

            postfix += formattedRegEx[i]
            postfix += formattedRegEx[i + 1]
            i += 1

            continue

        char = formattedRegEx[i]

        if char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()
        elif char not in precedence:
            postfix += char

        else:
            while (len(stack)):
                peekedChar = stack[-1]
                peekedCharPrecedence = precedence[peekedChar]
                currentCharPrecedence = precedence[char]
                if peekedCharPrecedence >= currentCharPrecedence:
                    postfix += stack.pop()
                else:
                    break
            stack.append(char)

    while (len(stack) > 0):
        postfix += stack.pop()

    return postfix


