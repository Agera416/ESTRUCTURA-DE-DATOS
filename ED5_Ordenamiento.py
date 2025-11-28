
from typing import List

# -----------------------------
# Ordenamiento Burbuja (Bubble)
# -----------------------------

def burbuja_verbose(arr: List[int]) -> List[int]:
    """Ordenamiento burbuja con salida paso a paso.

    Para cada pasada se compara pares adyacentes y se intercambian si están
    en el orden incorrecto. Después de cada intercambio se imprime el estado
    de la lista. También se muestra el estado al final de cada pasada.
    """
    n = len(arr)
    print("\n--- Burbuja: inicio ---")
    print("Lista inicial:", arr)

    # Convertir a copia para no modificar la lista original pasada por referencia
    lista = arr.copy()

    for i in range(n - 1):
        print(f"\nPasada {i + 1} (comprobando índices 0..{n-2-i}):")
        swapped = False
        for j in range(0, n - 1 - i):
            print(f"  Comparando lista[{j}]={lista[j]} y lista[{j+1}]={lista[j+1]}", end='')
            if lista[j] > lista[j + 1]:
                # intercambio
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                swapped = True
                print(f" -> intercambio -> {lista}")
            else:
                print(" -> sin cambio")
        print(f"Estado al final de la pasada {i + 1}: {lista}")
        if not swapped:
            print("No hubo intercambios en esta pasada: la lista ya está ordenada. Se detiene el algoritmo.")
            break

    print("Burbuja: lista ordenada final:", lista)
    return lista

# -----------------------------
# Ordenamiento Inserción
# -----------------------------

def insercion_verbose(arr: List[int]) -> List[int]:
    """Ordenamiento por inserción con salida paso a paso.

    Construye la lista ordenada insertando un elemento a la vez en su
    posición correcta. Se imprime el proceso de desplazamiento para cada
    elemento clave.
    """
    print("\n--- Inserción: inicio ---")
    print("Lista inicial:", arr)

    lista = arr.copy()
    n = len(lista)

    for i in range(1, n):
        key = lista[i]
        j = i - 1
        print(f"\nInsertando elemento en índice {i} (valor={key}) en la sublista ordenada 0..{i-1}:")
        print(f"  Estado antes: {lista}")

        # desplazar elementos mayores que key a la derecha
        while j >= 0 and lista[j] > key:
            print(f"  lista[{j}]={lista[j]} > key={key} -> desplazar lista[{j}] a la posición {j+1}")
            lista[j + 1] = lista[j]
            j -= 1
            print(f"  Estado intermedio: {lista}")

        lista[j + 1] = key
        print(f"  Colocar key en la posición {j+1}: {lista}")

    print("Inserción: lista ordenada final:", lista)
    return lista

# -----------------------------
# Ordenamiento Selección
# -----------------------------

def seleccion_verbose(arr: List[int]) -> List[int]:
    """Ordenamiento por selección con salida paso a paso.

    En cada iteración se busca el elemento mínimo en la parte no ordenada y
    se intercambia con la primera posición no ordenada. Se muestran las
    comparaciones y el intercambio cuando ocurre.
    """
    print("\n--- Selección: inicio ---")
    print("Lista inicial:", arr)

    lista = arr.copy()
    n = len(lista)

    for i in range(n - 1):
        min_idx = i
        print(f"\nIteración {i + 1}: buscar mínimo en la sublista índices {i}..{n-1}")
        for j in range(i + 1, n):
            print(f"  Comparando lista[{j}]={lista[j]} con lista[{min_idx}]={lista[min_idx]}", end='')
            if lista[j] < lista[min_idx]:
                min_idx = j
                print(f" -> nuevo mínimo en índice {min_idx}")
            else:
                print(" -> no cambia")

        # intercambiar el mínimo encontrado con la posición i
        if min_idx != i:
            print(f"  Intercambiar lista[{i}]={lista[i]} con lista[{min_idx}]={lista[min_idx]}")
            lista[i], lista[min_idx] = lista[min_idx], lista[i]
        else:
            print(f"  El mínimo ya está en la posición {i} (sin intercambio)")

        print(f"Estado al final de la iteración {i + 1}: {lista}")

    print("Selección: lista ordenada final:", lista)
    return lista

# -----------------------------
# Función auxiliar para leer lista desde input
# -----------------------------

def leer_lista_desde_input(texto: str) -> List[int]:
    """Lee una línea con números separados por espacios y devuelve lista de enteros.

    Si la entrada está vacía o es inválida, lanza ValueError.
    """
    partes = texto.strip().split()
    if not partes:
        raise ValueError("No se ingresaron números.")
    return [int(p) for p in partes]

# -----------------------------
# Menú principal
# -----------------------------

def menu_principal():
    ejemplo = [34, 12, 5, 66, 1]

    while True:
        print("\n================= MENÚ DE ORDENAMIENTOS =================")
        print("Elige un algoritmo (escribe el número):")
        print("1) Burbuja (paso a paso)")
        print("2) Inserción (paso a paso)")
        print("3) Selección (paso a paso)")
        print("4) Probar los 3 con la lista de ejemplo")
        print("0) Salir")

        opcion = input("Opción: ").strip()

        if opcion == '0':
            print("Saliendo. ¡Hasta luego!")
            break

        if opcion == '4':
            lista = ejemplo
            print("Usando lista de ejemplo:", lista)
            burbuja_verbose(lista)
            insercion_verbose(lista)
            seleccion_verbose(lista)
            continue

        if opcion not in {'1', '2', '3'}:
            print("Opción inválida. Intenta otra vez.")
            continue

        # pedir lista al usuario
        entrada = input("Introduce números separados por espacios (ej: 34 12 5 66 1) o deja vacío para usar la lista de ejemplo: ")
        if entrada.strip() == '':
            lista = ejemplo
            print("Usando lista de ejemplo:", lista)
        else:
            try:
                lista = leer_lista_desde_input(entrada)
            except ValueError as e:
                print("Entrada inválida:", e)
                continue

        if opcion == '1':
            burbuja_verbose(lista)
        elif opcion == '2':
            insercion_verbose(lista)
        elif opcion == '3':
            seleccion_verbose(lista)

# -----------------------------
# Ejecución directa
# -----------------------------

if __name__ == '__main__':
    menu_principal()
