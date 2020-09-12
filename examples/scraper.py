from src import Parser
import requests

source = requests.get("https://example.com").content

html = Parser(source)

print(html.title.content)
print(html.title.parent.name)
