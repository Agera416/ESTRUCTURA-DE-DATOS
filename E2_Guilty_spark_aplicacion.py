from MyLinkedList import MyLinkedList


lista = MyLinkedList()


lista.append(10)
lista.append(20)
lista.prepend(5)
lista.insert(1, 7)

print("Lista actual:", lista)
print("Tamaño:", len(lista))


print("Buscar 20:", lista.search(20))
print("Buscar 100:", lista.search(100))


lista.delete(7)
print("Después de eliminar 7:", lista)

# Mostrar si está vacía
print("¿Está vacía?", lista.is_empty())

