letter = '''Dear <|name|>,
you are selected!
<|date|>'''

print(letter.replace("<|name|>", "Harry").replace("<|date|>", "03 July 2026"))


