def warshall(A):
    n = len(A)
    R = [fila[:] for fila in A]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                R[i][j] = R[i][j] or (R[i][k] and R[k][j])

    return R

# 1 = camino, 0 = no camino
matriz = [
    [1, 1, 0],
    [0, 1, 1],
    [0, 0, 1]
]

res = warshall(matriz)
for fila in res:
    print(fila)
