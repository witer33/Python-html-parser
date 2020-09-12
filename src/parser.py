#Witer33 HTML-Parser
from src.types import Tag, OpeningTag, ClosingTag, Text
import re

class Parser:

    source = None
    char_counter = 0
    token_counter = 0
    tags = []
    tokens = []
    current_level = 0

    @staticmethod
    def level_sort(tag):
        return tag.level

    def __init__(self, source: str):
        self.source = str(source)
        self.parse()

    def advance(self):
        self.char_counter += 1
        if len(self.source) >= self.char_counter:
            return self.source[self.char_counter - 1]
        return None

    def token_advance(self):
        self.token_counter += 1
        if len(self.tokens) >= self.token_counter:
            return self.tokens[self.token_counter - 1]
        return None

    def parse_string(self):
        char = self.advance()
        string = ""

        while(char):
            if char == '"':
                return string
            else:
                string += char
            char = self.advance()

    def parse_tag(self):
        char = self.advance()
        closer_tag = False
        in_args = False
        in_args_value = False
        tag_name = ""
        arg_name = ""
        arg_value = ""
        args = {}

        while(char):
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
                        string = self.parse_string()
                        arg_value = string
                    else:
                        arg_value += char
                else:
                    tag_name += char
            char = self.advance()

    def closing_tag_searcher(self, tag_name):
        reset_counter = self.token_counter
        token = self.token_advance()
        closing_needed = 1

        while(token):

            if isinstance(token, ClosingTag) and token.name == tag_name:
                closing_needed -= 1

            if closing_needed == 0:
                self.token_counter = reset_counter
                return False

            if isinstance(token, OpeningTag) and token.name == tag_name:
                closing_needed += 1

            token = self.token_advance()
        
        self.token_counter = reset_counter
        return True

    def token_parser(self):
        token = self.token_advance()

        while(token):
            if isinstance(token, OpeningTag):
                token.self_enclosing = self.closing_tag_searcher(token.name)
            token = self.token_advance()

        self.token_counter = 0
        token = self.token_advance()
        opened_tags = []

        while(token):

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

            token = self.token_advance()
        self.token_counter = 0

    def parse(self):
        char = self.advance()
        current_text = ""

        while(char):

            if char == "<":
                if len(self.tokens) > 0:
                    self.tokens.append(Text(current_text))
                current_text = ""
                token = self.parse_tag()
                self.tokens.append(token)
            else:
                current_text += char

            char = self.advance()
        
        self.token_parser()

        self.token_counter = 0
        token = self.token_advance()

        while(token):

            if isinstance(token, OpeningTag):
                index = len(self.tags)
                self.tags.append(Tag(self, token.name, token.args, level=token.level, content=token.content, self_enclosing=token.self_enclosing, index=index))

            token = self.token_advance()

    def find(self, name: str, after: int = 0, args: list = {}, reverse: bool = False, level: int = None, **args2):

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
                return tag

    def find_all(self, name: str, after: int = 0, args: list = {}, reverse: bool = False, level: int = None, **args2):

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
                results.append(tag)
        if len(results) > 0:
            return results
        else:
            return

    def __getattr__(self, name):
        return self.find(name)

    def __getitem__(self, name):
        return self.find(name)
