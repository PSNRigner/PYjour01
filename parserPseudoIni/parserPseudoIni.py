from pyrser import grammar, parsing, meta


class parserPseudoIni(grammar.Grammar):
    entry = "Ini"
    grammar = """
    Ini = [ [Section:s #add_sec(_, s)]+ eof ]
    Section = [ '[' id:s ']' [ClefValeur:kv #add_kv(_, s, kv)]+ ]
    ClefValeur = [ id:s '=' valeur:v #is_pair(_, s, v) ]
    valeur = [ id:s #is_string(_, s) | num:n #is_num(_, n) | string:s #is_string(_, s) ]
    """

    def after_parse(self, node: parsing.Node):
        setattr(node, 'sections', node.node)
        return node


@meta.hook(parserPseudoIni)
def is_num(self, ast, arg):
    ast.node = str(int(self.value(arg)))
    return True


@meta.hook(parserPseudoIni)
def is_string(self, ast, arg):
    ast.node = self.value(arg)
    return True


@meta.hook(parserPseudoIni)
def add_kv(self, ast, s, arg):
    if not hasattr(ast, 'node'):
        ast.node = {}
    st = self.value(s)
    if not st in ast.node.keys():
        ast.node[st] = {}
    ast.node[st][arg.node[0]] = arg.node[1]
    return True


@meta.hook(parserPseudoIni)
def is_pair(self, ast, s, v):
    ast.node = (self.value(s).strip('"'), v.node)
    return True


@meta.hook(parserPseudoIni)
def add_sec(self, ast, arg):
    if not hasattr(ast, 'node'):
        ast.node = {}
    for key in arg.node.keys():
        ast.node[key] = arg.node[key]
    return True
