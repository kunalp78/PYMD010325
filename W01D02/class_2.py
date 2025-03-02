# integer
a = 23
print(type(a))
print(id(a))
b = 23
print(id(b))

a = "siva"
b = "siva"
print(id(a))
print(id(b))

a = [1, 2]
b = [1, 2]
# print(a == b)
print(id(a))
print(id(b))
print(a is b)

a = "siva"
b = "siva"
print(id(a))
print(id(b))
print(a is b)


t1 = (1, 2)
t2 = (1, 2)

print(t1 == t2)
print(id(t1))
print(id(t2))
print(t1 is t2)
