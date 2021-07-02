from django import template
register=template.Library()

@register.filter(name="_reverse")#这个过滤器翻转list
def _reverse(arg):
    return reversed(arg)
@register.filter(name="_breakimg")#通过!#!断开数个图片链接
def _breakimg(arg):
    if(arg==None):
        return
    return arg.split("!#!")    