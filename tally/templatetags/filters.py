
from django.template.defaulttags import register

# change the django forms label_tag to use classes instead of the default
@register.filter(is_safe=True)
def label_with_classes(value, arg):

    return value.label_tag(attrs={'class': arg})