def rem(l, word):
    for item in l:
        if item == word:
            l.remove(item)
    return l
l = ["harsh", "reena", "meow", "jahanvi"]
print(rem(l, "meow"))