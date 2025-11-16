import heapq

def dijkstra(grafo, origen):
    dist = {n: float('inf') for n in grafo}
    dist[origen] = 0
    cola = [(0, origen)]

    while cola:
        dist_actual, nodo = heapq.heappop(cola)

        for vecino, peso in grafo[nodo]:
            nueva = dist_actual + peso
            if nueva < dist[vecino]:
                dist[vecino] = nueva
                heapq.heappush(cola, (nueva, vecino))

    return dist

# Ejemplo de uso
grafo = {
    'A': [('B', 3), ('C', 1)],
    'B': [('D', 2)],
    'C': [('B', 1), ('D', 4)],
    'D': []
}

print(dijkstra(grafo, 'A'))
