
class Node:
    """Clase que representa un nodo en la lista enlazada"""
    def __init__(self, data):
        self.data = data
        self.next = None  # referencia al siguiente nodo

    def __repr__(self):
        return f"Node({self.data})"


class MyLinkedList:
    """Clase que representa una lista enlazada simple"""
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        """Verifica si la lista está vacía"""
        return self.head is None

    def append(self, data):
        """Agrega un nodo al final de la lista"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def prepend(self, data):
        """Agrega un nodo al inicio de la lista"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def insert(self, index, data):
        """Inserta un nodo en una posición específica"""
        if index < 0 or index > self.size:
            raise IndexError("Índice fuera de rango")
        if index == 0:
            self.prepend(data)
            return
        new_node = Node(data)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self.size += 1

    def delete(self, data):
        """Elimina el primer nodo que contenga el valor indicado"""
        current = self.head
        previous = None
        while current:
            if current.data == data:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                self.size -= 1
                return True
            previous = current
            current = current.next
        return False

    def search(self, data):
        """Busca un valor en la lista"""
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def __len__(self):
        """Devuelve el tamaño de la lista"""
        return self.size

    def __repr__(self):
        """Representación en cadena de la lista"""
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        return " -> ".join(nodes) + " -> None"

