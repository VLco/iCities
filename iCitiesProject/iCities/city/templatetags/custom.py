from django.template.defaulttags import register

...


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_keys(dictionary):
    return dictionary.keys()

@register.filter
def subtract(num1, num2):
    return num1 - num2
