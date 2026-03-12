import re

TOKEN_RE = re.compile(r"""
    \s+ |                 
    [A-Za-z_]\w* |         
    \d+ |                  
    ==|!=|<=|>= |          
    "[^"]*"|'[^']*' |      
    [+\-*"'/=(){};,.<>]
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