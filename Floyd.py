def floyd_warshall(g):
    dist = [fila[:] for fila in g]
    n = len(g)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist

INF = 999999
grafo = [
    [0, 3, INF, 5],
    [2, 0, INF, 4],
    [INF, 1, 0, INF],
    [INF, INF, 2, 0]
]

res = floyd_warshall(grafo)
for fila in res:
    print(fila)
