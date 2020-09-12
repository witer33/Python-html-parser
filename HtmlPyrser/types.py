# Python HTML Parser - A simple, fast and pure-python HTML parser
# Copyright (C) 2020-2021 witer33 <https://github.com/witer33>
#
# This file is part of Python HTML Parser.
#
# Python HTML Parser is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Python HTML Parser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Python HTML Parser.  If not, see <http://www.gnu.org/licenses/>.


class Tag:
    """
    A generic wrapper class around an HTML tag
    """

    def __init__(self, suorce, name: str, args: dict, level: int = 0, parent = None, childs: list = [], one_tag: bool = False, content: str = "", self_enclosing: bool = False, index: int = 0):
        self.name = name.lower()
        self.args = args
        self.level = level
        self.one_tag = one_tag
        self.content = content
        self.args["tag_content"] = content
        self.source = suorce
        self.index = index
        self.self_enclosing = False

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Tag: {self.name}"

    def __getattr__(self, name: str):
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

    def find_all(self, name: str, args: list = {}, **args2):
        return self.source.find_all(name, self.index, args, **args2)

    def get_parent(self):
        return self.source.find(None, self.index, reverse=True, level=(self.level - 1))


class OpeningTag:

    def __init__(self, name: str, args: str):
        self.name = name.lower()
        self.args = args
        self.self_enclosing = False
        self.content = ""


class ClosingTag:

    def __init__(self, name: str):
        self.name = name.lower()


class Text:

    def __init__(self, text: str):
        self.content = text
