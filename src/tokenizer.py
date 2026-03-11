import re

TOKEN_RE = re.compile(r"""
    \s+ |            # whitespace (we gonna ignore dis)
    [A-Za-z_]\w* |   # identifiers
    \d+ |            # numbers
    ==|!=|<=|>= |    # multi-char ops
    [+\-*"'/=(){};,.]   # single-char tokens
""", re.VERBOSE)

def getTokens(f):
    code = ''.join(getFileContents(f))
    tokens = TOKEN_RE.findall(code)
    print(tokens)
    return tokens

def getFileContents(path):
    if not path:
        return
    with open(path, "r") as f:
        return f.read()