# -*- coding:gbk -*-
from functools import wraps

def deco(func):
    @wraps(func) #固定原函数名、doc(不加，被deco装饰的函数的name和doc将会改成_deco/_deco2doc)
    def _deco(*args, **kwargs):
        '''_deco2doc'''
        print("before------called.")
        ret =func(*args, **kwargs)
        print("  after---------called.")
        return ret

    return _deco


@deco
def myfunc(a, b):
    print(" myfunc(%s,%s) called." % (a, b))
    return a + b

@deco
def myfunc2(a, b,c):
    '''func2doc'''
    print(" myfunc2(%s,%s,%s) called." % (a, b,c))
    return a + b + c


print myfunc(1, 2)
print myfunc2(3, 4,5)


print myfunc2.__name__
print myfunc2.__doc__







# def deco(func):
#     def _deco():
#         print("before myfunc() called.")
#         ret=func()
#         print("  after myfunc() called.")
#         return ret
#     return _deco
#
# @deco
# def myfunc():
#     print(" myfunc() called.")
#     return 'ok'
#
# print myfunc()




# def deco(func):
#     print("before myfunc() called.")
#     func()
#     print("  after myfunc() called.")
#     return func
#
#
# @deco
# def myfunc():
#     print(" myfunc() called.")
#
# myfunc()  ########### 问题 myfunc()执行两次


# def deco(func):
#     print("before myfunc() called.")
#     func()
#     print("  after myfunc() called.")
#     return func
#
#
# def myfunc():
#     print(" myfunc() called.")
#
#
# myfunc = deco(myfunc)