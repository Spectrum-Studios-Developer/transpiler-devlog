import re

TOKEN_RE = re.compile(r"""
    \s+ |                  # whitespace (ignore)
    [A-Za-z_]\w* |         # identifiers
    \d+ |                  # numbers
    ==|!=|<=|>= |          # multi-char ops
    "[^"]*"|'[^']*' |      # string literals
    [+\-*"'/=(){};,.]      # single-char tokens
""", re.VERBOSE)

def getTokens(f):
    code = getFileContents(f)
    tokens = [t for t in TOKEN_RE.findall(code) if not t.strip() == '']
    return tokens

def getFileContents(path):
    if not path:
        return
    with open(path, "r") as f:
        return f.read()