from src import Parser
import requests

suorce = requests.get("https://example.com").content

html = Parser(suorce)

print(html.title.content)
print(html.title.parent.name)
