def var2listsort(*args):
    tab = []

    for n in args:
        tab.append(n)

    j = 0
    while j < len(tab) - 1:
        i = 0
        while i < len(tab) -1:
            if tab[i] > tab[i + 1]:
                tmp = tab[i]
                tab[i] = tab[i + 1]
                tab[i + 1] = tmp
            i += 1
        j += 1
    return tab


class Bidon:
    num = 42
    zaz = "je suis un pro du python"

    def __init__(self, msg, num=42, **args):
        self.txt = msg
        self.num = num
        for arg in args:
            setattr(self, arg, args[arg])
