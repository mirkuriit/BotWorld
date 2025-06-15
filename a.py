import copy


class A:
    def __init__(self, m):
        self.m = m

    def copy(self):
        return copy.deepcopy(self)

a = A(m=1)
print(a.m)
b = a.copy()
print(b.m)

A.m = 90

print(A.m)
print(b.m)
