import re

TOKEN_SPEC = [
    ("WHITESPACE", r"\s+"),
    
    # comments
    ("COMMENT", r"//.*"),
    
    # multi-char operators (ALWAYS before single char)
    ("OP", r"==|!=|<=|>=|->|\+\+|--|\+=|-=|\*=|/="),

    # numbers
    ("FLOAT", r"\d+\.\d+"),
    ("INT", r"\d+"),

    # identifiers
    ("IDENT", r"[A-Za-z_]\w*"),

    # strings
    ("STRING", r'"[^"]*"|\'[^\']*\''),

    # single char symbols
    ("SYMBOL", r"[+\-*/=(){};,.<>#]"),
]

MASTER_RE = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
)

def tokenize(code):
    tokens = []

    for match in MASTER_RE.finditer(code):
        kind = match.lastgroup
        value = match.group()

        if kind in ("WHITESPACE", "COMMENT"):
            continue

        tokens.append(value)

    return tokens


def getFileContents(path):
    if not path:
        return
    with open(path, "r") as f:
        return f.read()


def getTokens(path):
    code = getFileContents(path)
    return tokenize(code)