class Tag:

    def __init__(self, suorce, name: str, args: dict, level: int = 0, parent = None, childs: list = [], one_tag: bool = False, content: str = "", self_enclosing: bool = False, index: int = 0):
        self.name = name.lower()
        self.args = args
        self.level = level
        self.one_tag = one_tag
        self.content = content
        self.source = suorce
        self.index = index
        self.self_enclosing = False

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return f"Tag: {self.name}"

    def __getattr__(self, name):
        if name == "parent":
            return self.get_parent()
        arg = self.args.get(name, None)
        if arg:
            return arg
        else:
            return self.find(name)

    def __getitem__(self, name):
        arg = self.args.get(name, None)
        if arg:
            return arg
        else:
            return self.find(name)

    def next(self):
        return self.source.tags[self.index + 1]

    def find(self, name: str, args: list = {}, **args2):
        return self.source.find(name, self.index, args, **args2)
    
    def get_parent(self):
        return self.source.find(None, self.index, reverse=True, level=(self.level - 1))

class OpeningTag:

    def __init__(self, name: str, args: str):
        self.name = name.lower()
        self.args = args
        self.self_enclosing = False
        self.content = ""

class ClosingTag:

    name = None

    def __init__(self, name: str):
        self.name = name.lower()

class Text:

    content = None

    def __init__(self, text: str):
        self.content = text
