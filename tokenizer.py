import re

index = 0
fileName = input(" > ")

TOKEN_RE = re.compile(r"""
    [A-Za-z_]\w* |   
    \d+ |            
    ==|!=|<=|>= |    
    [+\-*/=(){};,]   
""", re.VERBOSE)
def getTokens():
    data = ''.join(getFileContents())
    parts = data.split(';')
    return [line for part in parts for line in part.splitlines() if line.strip()]

def getFileContents():
    with open(fileName, "r") as f:
        return f.read()

def main():
    print(getTokens())

if __name__ == '__main__':
    main()