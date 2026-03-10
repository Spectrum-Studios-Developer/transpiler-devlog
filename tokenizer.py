import re

TOKEN_RE = re.compile(r"""
    [A-Za-z_]\w* |   
    \d+ |            
    ==|!=|<=|>= |    
    [+\-*/=(){};,.]   
""", re.VERBOSE)
def getTokens(f):
    code = ''.join(getFileContents(f))
    return TOKEN_RE.findall(code)      

def getFileContents(f):
    if not f:
        return
    with open(f, "r") as f:
        return f.read()