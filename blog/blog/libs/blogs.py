#-*- coding:utf-8 -*-

substitute = [
    (u'ç', 'c'),
    (u'ã', 'a'),
    (u'á', 'a'),
    (u'â', 'a'),
    (u'é', 'e'),
    (u'ê', 'e'),
    (u'ô', 'o'),
    (u'ó', 'o'),
    (u'õ', 'o'),
    (u'í', 'i'),
    (u'ú', 'u'),
    (u'ü', 'u'),
]

def removeAccents(text):
    for t, f in substitute:
        text = text.replace(t, f)
        text = text.replace(t.upper(), f.upper())
    return text


def titlelize(title):
    from string import letters, digits
    title = removeAccents(title)
    newtitle = ''
    acceptedchars = letters+digits
    for l in title:
        if l == ' ':
            newtitle += '-'
        elif l in acceptedchars:
            newtitle += l

    return newtitle.lower()