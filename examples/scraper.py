from PyHTML.parser import Parser
import requests


source = requests.get("https://example.com").content  # Fetch some HTML page
html = Parser(str(source))   # .content is of type bytes, but source must be a string!
html.parse()
print(html.title.content)
print(html.title.parent.name)
