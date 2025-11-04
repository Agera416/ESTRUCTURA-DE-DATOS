
import tkinter as tk
from tkinter import messagebox, simpledialog
import math

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insertar(self, key):
        if self.root is None:
            self.root = Node(key)
            return True
        curr = self.root
        while True:
            if key == curr.key:
                return False
            elif key < curr.key:
                if curr.left is None:
                    curr.left = Node(key)
                    return True
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = Node(key)
                    return True
                curr = curr.right

    def buscar(self, key):
        curr = self.root
        while curr:
            if key == curr.key:
                return curr
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def eliminar(self, key):
        def _delete_node(node, key):
            if node is None: return None
            if key < node.key:
                node.left = _delete_node(node.left, key)
            elif key > node.key:
                node.right = _delete_node(node.right, key)
            else:
                if node.left is None: return node.right
                if node.right is None: return node.left
                temp = node.right
                while temp.left: temp = temp.left
                node.key = temp.key
                node.right = _delete_node(node.right, temp.key)
            return node
        self.root = _delete_node(self.root, key)

    def eliminar_rama(self, key):
        node = self.buscar(key)
        if node:
            node.left = None
            node.right = None
            return True
        return False

    def eliminar_arbol(self):
        self.root = None

class TreeCanvas(tk.Canvas):
    NODE_RADIUS = 25
    LEVEL_HEIGHT = 100

    def __init__(self, parent, bst, **kwargs):
        super().__init__(parent, **kwargs)
        self.bst = bst
        self.width = int(self['width'])
        self.height = int(self['height'])
        self.bind('<Configure>', lambda e: self.redibujar())

    def redibujar(self):
        self.delete('all')
        if self.bst.root:
            self._draw_node(self.bst.root, self.width // 2, 50, self.width // 4)

    def _draw_node(self, node, x, y, x_offset):
        if node.left:
            x_left = x - x_offset
            y_child = y + self.LEVEL_HEIGHT
            self.create_line(x, y, x_left, y_child, width=2, fill='green')
            self._draw_node(node.left, x_left, y_child, x_offset // 2)
        if node.right:
            x_right = x + x_offset
            y_child = y + self.LEVEL_HEIGHT
            self.create_line(x, y, x_right, y_child, width=2, fill='green')
            self._draw_node(node.right, x_right, y_child, x_offset // 2)
        # Nodo con gradiente de color
        color = f'#{hex(150 + (node.key % 105))[2:]}aaff'
        self.create_oval(x - self.NODE_RADIUS, y - self.NODE_RADIUS, x + self.NODE_RADIUS, y + self.NODE_RADIUS, fill=color, outline='blue', width=2)
        self.create_text(x, y, text=str(node.key), font=('Arial', 12, 'bold'), fill='white')

class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Árbol Binario de Búsqueda Creativo')
        self.bst = BST()

        root.configure(bg='#f0f0f0')

        control_frame = tk.Frame(root, bg='#e0e0ff', pady=10)
        control_frame.pack(fill=tk.X)

        tk.Label(control_frame, text='Valor:', font=('Arial', 12, 'bold'), bg='#e0e0ff').pack(side=tk.LEFT, padx=5)
        self.entry = tk.Entry(control_frame, font=('Arial', 12), width=8)
        self.entry.pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text='Insertar', bg='#4caf50', fg='white', font=('Arial', 11, 'bold'), command=self.insertar).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text='Eliminar Nodo', bg='#f44336', fg='white', font=('Arial', 11, 'bold'), command=self.eliminar_nodo).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text='Eliminar Rama', bg='#ff9800', fg='white', font=('Arial', 11, 'bold'), command=self.eliminar_rama).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text='Eliminar Árbol', bg='#9c27b0', fg='white', font=('Arial', 11, 'bold'), command=self.eliminar_arbol).pack(side=tk.LEFT, padx=5)

        self.canvas = TreeCanvas(root, self.bst, width=900, height=700, bg='#ffffff')
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def insertar(self):
        val = self.entry.get().strip()
        if not val: return
        try: key = int(val)
        except: key = val
        self.bst.insertar(key)
        self.entry.delete(0, tk.END)
        self.canvas.redibujar()

    def eliminar_nodo(self):
        val = self.entry.get().strip()
        if not val: return
        try: key = int(val)
        except: key = val
        self.bst.eliminar(key)
        self.entry.delete(0, tk.END)
        self.canvas.redibujar()

    def eliminar_rama(self):
        val = self.entry.get().strip()
        if not val: return
        try: key = int(val)
        except: key = val
        self.bst.eliminar_rama(key)
        self.entry.delete(0, tk.END)
        self.canvas.redibujar()

    def eliminar_arbol(self):
        if messagebox.askyesno('Eliminar árbol', '¿Deseas eliminar todo el árbol?'):
            self.bst.eliminar_arbol()
            self.canvas.redibujar()

def main():
    root = tk.Tk()
    app = App(root)
    root.geometry('1000x800')
    root.mainloop()

if __name__=='__main__':
    main()
