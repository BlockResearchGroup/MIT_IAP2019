# variable
print('\n==========variable===========')
a = 5 / 2
print("a is 5/2: ", a)

a = a + 1  # add one
print("a is now: ", a)

b = a * 10  # b is a multiple 10

a, b = b, a  # swapping a with b
print("a is now: ", a)

# type
print('\n==========type===========')
print("the type of a is: ", type(a))

a = int(a)
print("the type of a is: ", type(a))

# list
print('\n==========list===========')
c = [1, 2, 4, 6, 10, 20]
print(c)
print(type(c))

c.append(1000)  # add item to the end
print(c)
c.pop()  # remove the last item
print(c)
print(c[0])  # show the first item
print(c[3])  # show the third item
print(c[-1])  # show the last item
print(c[2:])  # slice the list from 2
print(c[:-2])  # slice until the last 2

d = c[2:] + c[:-2]
print(d)
d.reverse()
print(d)
print(len(d))

# tuple
print('\n==========tuple===========')
e = (1, 2, 5)  # cannot append
print(e)
print(e[0])  # tuples are like lists but are immutable.
print(len(e))
print(e[1:])  # you can do all other things like list
print(5 in e)

# dictionary
print('\n==========dictionary===========')
f = {'e': 'ETH', 'a': 'apple', 'i': 'ice cream', 'num': [1, 2, 3]}
print(f)
print('a is: ', f['a'])
print('i is: ', f['i'])
print('num is: ', f['num'])
print(f.keys())
print(f.values())
print(f.items())  # Get all key-value pairs as a list of tuples

f['t'] = 'Tongji'
f['m'] = 'MIT'
print(f)

# set
print('\n==========set===========')
g = set(d)
h = {1, 2, 3, 4}
print(g, h)
print(g | h)  # union
print(g & h)  # intersection
print(g - h)  # difference
print(g ^ h)  # symmetric difference

# if else
print('\n==========if else===========')
if a < 10:
    print('a is smaller than 10, a is: ', a)
else:
    print('a is bigger than 10, a is: ', a)

# for loop
print('\n==========for loop===========')
d = []
for i in range(20):
    d.append(i)
print(d)

# while loop
print('\n==========while loop===========')
i, d = 0, []
while i < a:
    d.append(i)
    i += 1
print(d)

# function def
print('\n==========function===========')


def add(a, b):
    return a + b


print(add(10, 100))

for i in range(10):
    print('hello')


def print_with_newline(text):
    print('workshop')
    print(text, '\n')
    # not return value, just some action here


for i in range(10):
    print_with_newline('hello')

# def all_the_args(*args, **kwargs):
print('\n==========arg===========')


def varargs(*args):
    return args


def keyword_args(**kwargs):
    return kwargs


j = varargs(1, 2, 4)
print(j)

k = keyword_args(edge="edge", node="vertice")
print(k)


def all_the_args(*args, **kwargs):
    print(args)
    print(kwargs)


args = (1, 2, 4)
kwargs = {"edge": "edge", "node": "vertice"}

all_the_args(*args)
all_the_args(**kwargs)
all_the_args(*args, **kwargs)


def pass_all_the_args(*args, **kwargs):
    all_the_args(*args, **kwargs)
    print(varargs(*args))
    print(keyword_args(**kwargs))


# call back function
print('\n==========callback===========')


def callback(sum):
    print("Sum = {}".format(sum))


def add_with_callback(a, b, callback=None):
    print("adding {} + {}".format(a, b))
    if callback:
        callback(a + b)


add_with_callback(1, 2, callback)
