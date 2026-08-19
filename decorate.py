import functools


def log(fun):
    @functools.wraps(fun)
    def wraper(*args,**kawrds):
        print("%s" % fun.__name__)
        return fun(*args,**kawrds)
    return wraper
@log
def fun(x,y):
    print("%d+%d=%d"%(x,y,x+y))
fun(1,y=8)
print("%s" % fun.__name__)