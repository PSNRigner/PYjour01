from pyrser import grammar, parsing, meta


class parserCSV(grammar.Grammar):
    entry = "Csv"
    grammar = """
        Csv = [ [ [ id:s #is_string(_, s) | ';':s #is_string(_,s) | '\n':s #is_string(_,s) ]+ ]+ eof ]
        """

    def __init__(self):
        super().__init__()
        self.pop_ignore()

    def after_parse(self, node: parsing.Node):
        if not hasattr(node, 'words'):
            node.words = []
        if not hasattr(node, 'lines'):
            node.lines = []
        if len(node.words) != 0:
            group(node)
        return node


@meta.hook(parserCSV)
def is_string(self, ast, s):
    word = self.value(s)
    if not hasattr(ast, 'words'):
        ast.words = []
    if not hasattr(ast, 'lines'):
        ast.lines = []
    if word == "\n":
        if hasattr(ast, 'next') and ast.next:
            ast.words.append('')
        group(ast)
        ast.next = False
        return True
    if word == ";":
        if hasattr(ast, 'next') and ast.next:
            word = ""
        else:
            if len(ast.words) == 0:
                ast.words.append('')
            ast.next = True
            return True
    else:
        ast.next = False
    ast.words.append(word)
    return True


def group(ast):
    tab = ast.words.copy()
    ast.words.clear()
    ast.lines.append(tab)
