class UnionFind:
    def __init__(self, n):
        self.padre = list(range(n))

    def find(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.find(self.padre[x])
        return self.padre[x]

    def union(self, a, b):
        raizA = self.find(a)
        raizB = self.find(b)
        if raizA != raizB:
            self.padre[raizB] = raizA
            return True
        return False

def kruskal(n, aristas):
    uf = UnionFind(n)
    mst = []
    aristas.sort(key=lambda x: x[2])

    for u, v, w in aristas:
        if uf.union(u, v):
            mst.append((u, v, w))
    return mst

aristas = [
    (0, 1, 4),
    (0, 2, 3),
    (1, 2, 1),
    (1, 3, 2),
    (2, 3, 4)
]

print(kruskal(4, aristas))
