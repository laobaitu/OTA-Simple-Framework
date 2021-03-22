import json

def f(x):
    return x * x

d = {
    'a' : f,
    'b' : f
}

print(d['a'](3))