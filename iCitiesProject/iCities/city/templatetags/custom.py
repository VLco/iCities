from django.template.defaulttags import register

...


@register.filter
def next(some_list, current_index):
    """
    Returns the next element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    try:
        return some_list[int(current_index) + 1] # access the next element
    except:
        return '' # return empty string in case of exception


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_keys(dictionary):
    return dictionary.keys()

@register.filter
def subtract(num1, num2):
    return num1 - num2

@register.filter
def sumVal(dictionary):
    sum = 0
    for i in dictionary.values():
        print(type(i.getValDec))
        print()
    return sum
