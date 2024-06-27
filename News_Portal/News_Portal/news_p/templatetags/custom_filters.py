from django import template

register = template.Library()

CENS_LIST = ['сука', 'дурак', 'тварь', 'тупой', ]


@register.filter()
def censor(value):
    if type(value) != str:
        raise TypeError('Необходимо передать строку!')
    else:
        for word in value.split():
            if word.lower() in CENS_LIST:
                cens_word = word[0] + ((len(word) - 1) * '*')
                value = value.replace(word, cens_word)
    return value

