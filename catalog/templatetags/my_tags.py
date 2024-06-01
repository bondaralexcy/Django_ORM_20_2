# Пользовательский тег и фильтр

import datetime
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

register = template.Library()


# Создание тега, преобразующего текущую дату в заданный формат
@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


# Создание фильтра, который ВЫДЕЛЯЕТ первый символ строки (Буквица):
@register.filter(needs_autoescape=True)
def initial_letter_filter(text, autoescape=True):
    # return mark_safe(text)

    first, other = text[0], text[1:]
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = "<strong>%s</strong>%s" % (esc(first), esc(other))
    return mark_safe(result)


# Создание фильтра, добавляющего актуальный путь до каталога с рисунками
@register.filter()
def media_filter(data):
    if data:
        return f"/media/product/{data}"
    return "#"
