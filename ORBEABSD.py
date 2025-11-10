"""
tarea_grafos_mapa_grande_v2.py

Versión ampliada y corregida:
- Mapa más grande y claro.
- Nodos y aristas más visibles.
- Coordenadas ajustadas para Tabasco, CDMX y Edomex.
"""

import itertools
import math
import matplotlib.pyplot as plt
import networkx as nx
from PIL import Image
import urllib.request
import numpy as np

# --------------------------
# Definición de estados y grafo
# --------------------------
STATES = ["CDMX", "Edomex", "Puebla", "Veracruz", "Oaxaca", "Chiapas", "Tabasco"]

GRAPH = {
    "CDMX":    {"Edomex": 40, "Puebla": 130, "Veracruz": 350},
    "Edomex":  {"CDMX": 40, "Puebla": 110, "Veracruz": 330},
    "Puebla":  {"CDMX": 130, "Edomex": 110, "Veracruz": 290, "Oaxaca": 520},
    "Veracruz":{"CDMX": 350, "Edomex": 330, "Puebla": 290, "Tabasco": 560, "Oaxaca": 700},
    "Oaxaca":  {"Puebla": 520, "Veracruz": 700, "Chiapas": 470},
    "Chiapas": {"Oaxaca": 470, "Tabasco": 280},
    "Tabasco": {"Veracruz": 560, "Chiapas": 280},
}

# --------------------------
# Coordenadas corregidas (latitud, longitud)
# --------------------------
coords = {
    "CDMX": (19.4326, -99.1332),     # Ciudad de México
    "Edomex": (19.37, -99.75),       # Zona Toluca
    "Puebla": (19.04, -98.20),
    "Veracruz": (19.17, -96.13),
    "Oaxaca": (17.06, -96.72),
    "Chiapas": (16.75, -93.12),
    "Tabasco": (17.99, -92.93),      # Villahermosa corregido
}

# --------------------------
# Funciones de cálculo
# --------------------------
INF = 10**9

def cost(u, v):
    return GRAPH.get(u, {}).get(v, INF)

def find_hamiltonian_paths(states):
    results = []
    for perm in itertools.permutations(states):
        total = 0
        valid = True
        for i in range(len(states)-1):
            c = cost(perm[i], perm[i+1])
            if c >= INF:
                valid = False
                break
            total += c
        if valid:
            results.append((list(perm), total))
    return results

def floyd_warshall_with_next(nodes):
    idx = {v:i for i,v in enumerate(nodes)}
    n = len(nodes)
    dist = [[INF]*n for _ in range(n)]
    nxt = [[None]*n for _ in range(n)]
    for i,u in enumerate(nodes):
        dist[i][i] = 0
        nxt[i][i] = u
        for v,w in GRAPH.get(u, {}).items():
            j = idx[v]
            dist[i][j] = w
            nxt[i][j] = v
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    return dist, nxt, idx

def tsp_path_minimum(nodes, dist):
    n = len(nodes)
    ALL = 1<<n
    DP = [[INF]*n for _ in range(ALL)]
    parent = [[(-1,-1)]*n for _ in range(ALL)]
    for i in range(n):
        DP[1<<i][i] = 0
    for mask in range(ALL):
        for last in range(n):
            if DP[mask][last] >= INF: continue
            for nxt_node in range(n):
                if mask & (1<<nxt_node): continue
                newmask = mask | (1<<nxt_node)
                newcost = DP[mask][last] + dist[last][nxt_node]
                if newcost < DP[newmask][nxt_node]:
                    DP[newmask][nxt_node] = newcost
                    parent[newmask][nxt_node] = (last, mask)
    full = ALL - 1
    best_cost = INF
    best_end = -1
    for end in range(n):
        if DP[full][end] < best_cost:
            best_cost = DP[full][end]
            best_end = end
    if best_end == -1:
        return None, None
    route_idx = []
    cur_mask = full
    cur = best_end
    while cur != -1:
        route_idx.append(cur)
        prev, prev_mask = parent[cur_mask][cur]
        cur = prev
        cur_mask = prev_mask
    route_idx.reverse()
    return best_cost, [nodes[i] for i in route_idx]

# --------------------------
# Mostrar resultados
# --------------------------
def solve_and_show():
    print("Estados:", STATES)
    print("Relaciones:")
    for u in STATES:
        for v,w in GRAPH[u].items():
            if u <= v:
                print(f"  {u} - {v}: {w} km")

    print("\n(a) Recorrido sin repetir:")
    paths = find_hamiltonian_paths(STATES)
    if not paths:
        print("  No hay camino hamiltoniano directo.")
    else:
        best = min(paths, key=lambda x:x[1])
        print(f"  Mejor ruta: {' -> '.join(best[0])}")
        print(f"  Costo total: {best[1]} km")

    print("\n(b) Recorrido repitiendo al menos un estado:")
    dist, nxt, idx = floyd_warshall_with_next(STATES)
    best_cost, best_route = tsp_path_minimum(STATES, dist)
    print(f"  Mejor ruta (orden principal): {' -> '.join(best_route)}")
    print(f"  Costo mínimo total: {best_cost} km")

# --------------------------
# Dibuja el grafo sobre el mapa (grande y con posiciones corregidas)
# --------------------------
def draw_graph_on_map():
    map_url = "https://media.istockphoto.com/id/1161574561/es/vector/ilustraci%C3%B3n-aislada-vectorial-del-mapa-administrativo-simplificado-de-m%C3%A9xico-fronteras.jpg?s=612x612&w=0&k=20&c=MCX9BZWvSjc57ae0_cH2RfFtTo1tf9GlqVoJn1xj5ek="
    with urllib.request.urlopen(map_url) as url:
        img = Image.open(url)
        img = np.array(img)

    G = nx.Graph()
    for u in GRAPH:
        for v, w in GRAPH[u].items():
            G.add_edge(u, v, weight=w)

    # (lon, lat) para ubicar correctamente
    pos = {s: (coords[s][1], coords[s][0]) for s in coords}

    plt.figure(figsize=(14, 12))
    plt.imshow(img, extent=[-117, -86, 14, 33], alpha=0.55)

    # Aristas
    nx.draw_networkx_edges(G, pos, width=2.5, edge_color="black", alpha=0.8)

    # Nodos
    nx.draw_networkx_nodes(G, pos, node_color="royalblue", node_size=2200, edgecolors="white")

    # Etiquetas de estados
    nx.draw_networkx_labels(G, pos, font_size=12, font_color="white", font_weight="bold")

    # Pesos
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="darkred", font_size=11, font_weight="bold")

    plt.title("Grafo de 7 estados sobre el mapa de México", fontsize=18, weight="bold", pad=20)
    plt.xlabel("Longitud", fontsize=13)
    plt.ylabel("Latitud", fontsize=13)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.show()

# --------------------------
# Programa principal
# --------------------------
if __name__ == "__main__":
    solve_and_show()
    draw_graph_on_map()
