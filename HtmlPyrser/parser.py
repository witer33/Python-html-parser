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


from .types import Tag, OpeningTag, ClosingTag, Text
from typing import Union
import re


class Parser:

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.token_count = 0
        self.tags = []
        self.tokens = []
        self.level = 0

    def advance(self):
        """
        Steps one character forward in self.source
        """

        self.pos += 1
        if len(self.source) >= self.pos:
            return self.source[self.pos - 1]
        return None

    def advance_token(self):
        """
        Steps one character forward in self.tokens
        """

        self.token_count += 1
        if len(self.tokens) >= self.token_count:
            return self.tokens[self.token_count - 1]
        return None

    def _parse_string(self):
        """
        Parses a string within its delimiters
        """

        char = self.advance()
        string = ""
        while char:
            if char == '"':
                return string
            else:
                string += char
            char = self.advance()

    def _parse_tag(self):
        """
        Parses an HTML tag
        """

        char = self.advance()
        closer_tag = False
        in_args = False
        in_args_value = False
        tag_name = ""
        arg_name = ""
        arg_value = ""
        args = {}
        while char:
            if char == "/":
                closer_tag = True
            elif char == " ":
                in_args = True
                in_args_value = False
                if arg_name != "":
                    args[arg_name] = arg_value
                arg_name = ""
                arg_value = ""
            elif char == "=":
                in_args = False
                in_args_value = True
            elif char == ">":
                if not closer_tag:
                    if arg_name != "":
                        args[arg_name] = arg_value
                    return OpeningTag(tag_name, args)
                else:
                    return ClosingTag(tag_name)
            else:
                if in_args:
                    arg_name += char
                elif in_args_value:
                    if char == '"':
                        string = self._parse_string()
                        arg_value = string
                    else:
                        arg_value += char
                else:
                    tag_name += char
            char = self.advance()

    def _find_closing_tag(self, tag_name: str) -> bool:
        """
        Finds a closing tag for the given tag_name
        """

        reset_counter = self.token_count
        token = self.advance_token()
        closing_needed = 1
        while token:
            if isinstance(token, ClosingTag) and token.name == tag_name:
                closing_needed -= 1
            if closing_needed == 0:
                self.token_count = reset_counter
                return False
            if isinstance(token, OpeningTag) and token.name == tag_name:
                closing_needed += 1
            token = self.advance_token()
        self.token_count = reset_counter
        return True

    def _parse_tokens(self):
        """
        Performs token parsing
        """

        token = self.advance_token()
        while token:
            if isinstance(token, OpeningTag):
                token.self_enclosing = self._find_closing_tag(token.name)
            token = self.advance_token()
        self.token_count = 0
        token = self.advance_token()
        opened_tags = []
        while token:
            if isinstance(token, OpeningTag) and not token.self_enclosing:
                token.level = len(opened_tags)
                opened_tags.append(token)
            elif isinstance(token, OpeningTag) and token.self_enclosing:
                token.level = len(opened_tags)
            elif isinstance(token, ClosingTag) and opened_tags[-1].name == token.name:
                del opened_tags[-1]
            elif isinstance(token, Text) and len(opened_tags) > 0:
                if token.content:
                    opened_tags[-1].content += token.content
            token = self.advance_token()
        self.token_count = 0

    def parse(self):
        """
        Parses self.source
        """

        char = self.advance()
        current_text = ""
        while char:
            if char == "<":
                if len(self.tokens) > 0:
                    self.tokens.append(Text(current_text))
                current_text = ""
                token = self._parse_tag()
                self.tokens.append(token)
            else:
                current_text += char
            char = self.advance()
        self._parse_tokens()
        self.token_count = 0
        token = self.advance_token()
        while token:
            if isinstance(token, OpeningTag) and token.name != "!--":
                index = len(self.tags)
                self.tags.append(Tag(self, token.name, token.args, level=token.level, content=token.content, self_enclosing=token.self_enclosing, index=index))
            token = self.advance_token()

    def find(self, name: str, after: int = 0, args: list = {}, reverse: bool = False, level: int = None, all: bool = False, **args2):
        results = []
        for tag in (self.tags[after:] if not reverse else self.tags[:after][::-1]):
            if tag.name == name or not name:
                breaked = False
                for arg, value in args.items():
                    if not isinstance(value, re.Pattern):
                        if value != tag.args.get(arg, ""):
                            breaked = True
                            break
                    else:
                        if not value.match(tag.args.get(arg, "")):
                            breaked = True
                            break
                for arg, value in args2.items():
                    if not isinstance(value, re.Pattern):
                        if value != tag.args.get(arg, ""):
                            breaked = True
                            break
                    else:
                        if not value.match(tag.args.get(arg, "")):
                            breaked = True
                            break
                if breaked:
                    continue
                if level:
                    if tag.level != level:
                        continue
                if not all:
                    return tag
                else:
                    results.append(tag)
        if all and len(results) > 0:
            return results
        else:
            return

    def find_all(self, name: str, after: int = 0, args: list = {}, reverse: bool = False, level: int = None, **args2):
        return self.find(name, after, args, reverse, level, True, **args2)

    def __getattr__(self, name):
        return self.find(name)

    def __getitem__(self, name):
        return self.find(name)
