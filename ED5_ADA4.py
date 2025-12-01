#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
busquedas_gui.py
Programa con GUI (tkinter) que permite ejecutar 3 métodos de búsqueda:
1) Secuencial
2) Binaria
3) Hash

Características principales:
- Impresión automática de elementos al seleccionar el método.
- Ordenación paso a paso (Bubble Sort) con impresión de comparaciones e intercambios.
- Permite cargar una lista personalizada (pegar números separados por comas/espacios/enter).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import re

# -------------------------
# Algoritmos de búsqueda
# -------------------------
def busqueda_secuencial(arr, target, verbose_callback=None):
    for i, val in enumerate(arr):
        if verbose_callback:
            verbose_callback(f"Comprobando índice {i}: valor {val}")
        if val == target:
            if verbose_callback:
                verbose_callback(f"Encontrado en índice {i}.")
            return i
    if verbose_callback:
        verbose_callback("No encontrado.")
    return -1

def busqueda_binaria(arr, target, verbose_callback=None):
    lo = 0
    hi = len(arr) - 1
    pasos = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        pasos += 1
        if verbose_callback:
            verbose_callback(f"Paso {pasos}: lo={lo}, hi={hi}, mid={mid}, arr[mid]={arr[mid]}")
        if arr[mid] == target:
            if verbose_callback:
                verbose_callback(f"Encontrado en índice {mid}.")
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    if verbose_callback:
        verbose_callback("No encontrado.")
    return -1

def busqueda_hash(arr, target, verbose_callback=None):
    tabla = {}
    for i, v in enumerate(arr):
        tabla.setdefault(v, []).append(i)
        if verbose_callback:
            verbose_callback(f"Insertando en hash: valor {v} -> índice {i}")
    if target in tabla:
        indices = tabla[target]
        if verbose_callback:
            verbose_callback(f"Encontrado en índice(s): {indices}")
        return indices
    else:
        if verbose_callback:
            verbose_callback("No encontrado en la tabla hash.")
        return []


# -------------------------
# Interfaz gráfica (tkinter)
# -------------------------
class BusquedasApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Busquedas - Secuencial | Binaria | Hash")
        self.geometry("820x540")
        self.resizable(False, False)

        # lista inicial aleatoria
        self.lista = [random.randint(0, 99) for _ in range(20)]
        self.metodos = ["Secuencial", "Binaria", "Hash"]

        # estado de ordenación animada
        self._sorting = False
        self._sort_actions = []

        self._create_widgets()
        self._update_lista_display()

    def _create_widgets(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=False)
        filemenu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Archivo", menu=filemenu)
        self.config(menu=menubar)

        toolbar = ttk.Frame(self, padding=(6,6))
        toolbar.pack(fill="x")

        ttk.Label(toolbar, text="Método:").pack(side="left", padx=(0,6))
        self.metodo_combo = ttk.Combobox(toolbar, values=self.metodos, state="readonly", width=12)
        self.metodo_combo.current(0)
        self.metodo_combo.pack(side="left")

        # cuando se selecciona un método → imprime elementos
        self.metodo_combo.bind("<<ComboboxSelected>>", self.mostrar_elementos)

        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=8)

        ttk.Label(toolbar, text="Valor a buscar:").pack(side="left")
        self.entry_valor = ttk.Entry(toolbar, width=10)
        self.entry_valor.pack(side="left", padx=(6,10))

        btn_buscar = ttk.Button(toolbar, text="Ejecutar búsqueda", command=self.ejecutar_busqueda)
        btn_buscar.pack(side="left", padx=6)

        btn_gen = ttk.Button(toolbar, text="Generar lista (aleatoria)", command=self.generar_lista)
        btn_gen.pack(side="left", padx=6)

        # Botón de ordenar ahora lanza la ordenación paso a paso
        btn_ordenar = ttk.Button(toolbar, text="Ordenar lista (para Binaria)", command=self.iniciar_ordenacion_paso)
        btn_ordenar.pack(side="left", padx=6)

        btn_cargar = ttk.Button(toolbar, text="Cargar lista personalizada", command=self.abrir_dialogo_cargar)
        btn_cargar.pack(side="left", padx=6)

        btn_limpiar = ttk.Button(toolbar, text="Limpiar salida", command=self.limpiar_salida)
        btn_limpiar.pack(side="left", padx=6)

        # guardamos referencias a algunos botones para habilitar/deshabilitar
        self._btn_ordenar = btn_ordenar
        self._btn_gen = btn_gen
        self._btn_buscar = btn_buscar
        self._btn_cargar = btn_cargar

        main = ttk.Frame(self, padding=(8,8))
        main.pack(fill="both", expand=True)

        left = ttk.Frame(main, width=300)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        ttk.Label(left, text="Lista actual (elementos):").pack(anchor="w")
        self.lista_text = tk.Text(left, width=30, height=24, state="disabled", wrap="none")
        self.lista_text.pack(fill="y", expand=True, pady=(6,0))

        right = ttk.Frame(main)
        right.pack(side="left", fill="both", expand=True, padx=(12,0))

        ttk.Label(right, text="Salida / Pasos:").pack(anchor="w")
        self.salida_text = tk.Text(right, wrap="word", state="disabled")
        self.salida_text.pack(fill="both", expand=True, pady=(6,0))

        self.status_var = tk.StringVar(value="Lista generada aleatoriamente.")
        status = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w")
        status.pack(side="bottom", fill="x")

    # -------------------------
    # Mostrar elementos al elegir método
    # -------------------------
    def mostrar_elementos(self, event=None):
        self.limpiar_salida()
        metodo = self.metodo_combo.get()
        self._append_salida(f"Método seleccionado: {metodo}")
        self._append_salida("Mostrando lista elemento por elemento:")
        self._append_salida("-" * 40)

        for i, v in enumerate(self.lista):
            self._append_salida(f"Índice {i:02d} → Valor: {v}")

        self.status_var.set("Elementos mostrados en la salida.")

    # -------------------------
    # Funciones UI existentes
    # -------------------------
    def _append_salida(self, texto):
        self.salida_text.config(state="normal")
        self.salida_text.insert("end", texto + "\n")
        self.salida_text.see("end")
        self.salida_text.config(state="disabled")

    def _update_lista_display(self, highlight_indices=None):
        """
        Actualiza la visualización textual de la lista en la columna izquierda.
        Si highlight_indices es una tupla/lista, marca esos índices con un marcador.
        """
        self.lista_text.config(state="normal")
        self.lista_text.delete("1.0", "end")
        for i, v in enumerate(self.lista):
            marker = ""
            if highlight_indices and i in highlight_indices:
                marker = "  <--"
            self.lista_text.insert("end", f"{i:02d}: {v}{marker}\n")
        self.lista_text.config(state="disabled")

    def limpiar_salida(self):
        self.salida_text.config(state="normal")
        self.salida_text.delete("1.0", "end")
        self.salida_text.config(state="disabled")
        self.status_var.set("Salida limpiada.")

    def generar_lista(self):
        if self._sorting:
            messagebox.showinfo("Ordenación en progreso", "Espera a que termine la ordenación antes de generar nueva lista.")
            return
        self.lista = [random.randint(0, 99) for _ in range(20)]
        self._update_lista_display()
        self.status_var.set("Lista generada aleatoriamente.")
        self._append_salida("Nueva lista generada.")

    # -------------------------
    # Cargar lista personalizada (dialog)
    # -------------------------
    def abrir_dialogo_cargar(self):
        if self._sorting:
            messagebox.showinfo("Ordenación en progreso", "Espera a que termine la ordenación antes de cargar otra lista.")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Cargar lista personalizada")
        dialog.geometry("420x300")
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(dialog, text="Pega o escribe números separados por comas, espacios o saltos de línea:").pack(anchor="w", padx=8, pady=(8,4))
        text_box = tk.Text(dialog, wrap="word", height=10)
        text_box.pack(fill="both", expand=True, padx=8)

        # ejemplo de formato prellenado
        text_box.insert("end", "e.g. 10, 5, 23, 7, 7, 42\n")

        def cargar_y_cerrar():
            contenido = text_box.get("1.0", "end").strip()
            try:
                nueva_lista = self._parsear_numeros(contenido)
            except ValueError as e:
                messagebox.showerror("Error al parsear", str(e), parent=dialog)
                return

            if len(nueva_lista) == 0:
                messagebox.showwarning("Lista vacía", "No se detectaron números válidos.", parent=dialog)
                return

            # limitar tamaño razonable para interfaz
            if len(nueva_lista) > 200:
                if not messagebox.askyesno("Lista grande", f"La lista tiene {len(nueva_lista)} elementos. ¿Deseas continuar?"):
                    return

            self.lista = nueva_lista
            self._update_lista_display()
            self.status_var.set(f"Lista personalizada cargada ({len(self.lista)} elementos).")
            self._append_salida(f"Lista personalizada cargada ({len(self.lista)} elementos).")
            dialog.destroy()

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill="x", pady=8, padx=8)
        ttk.Button(btn_frame, text="Cargar y cerrar", command=cargar_y_cerrar).pack(side="right", padx=(6,0))
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy).pack(side="right")

    def _parsear_numeros(self, texto: str):
        """
        Recibe un texto con números separados por comas, espacios, saltos de línea u otros separadores simples.
        Devuelve una lista de enteros o lanza ValueError en caso de token no numérico.
        """
        if not texto:
            return []
        # dividir por comas o espacios o saltos de línea
        tokens = re.split(r'[,\s]+', texto.strip())
        nums = []
        for t in tokens:
            if t == '':
                continue
            # permitir signo negativo
            if re.fullmatch(r'[+-]?\d+', t):
                nums.append(int(t))
            else:
                # token inválido: lanzar error con detalle
                raise ValueError(f"Token inválido encontrado: '{t}'. Usa solo números separados por comas, espacios o saltos de línea.")
        return nums

    # -------------------------
    # Ordenación paso a paso (Bubble Sort)
    # -------------------------
    def iniciar_ordenacion_paso(self):
        if self._sorting:
            return
        n = len(self.lista)
        actions = []
        arr_copy = list(self.lista)
        for i in range(n):
            for j in range(0, n - i - 1):
                actions.append(('compare', j, j+1, list(arr_copy)))
                if arr_copy[j] > arr_copy[j+1]:
                    arr_copy[j], arr_copy[j+1] = arr_copy[j+1], arr_copy[j]
                    actions.append(('swap', j, j+1, list(arr_copy)))
            actions.append(('pass_complete', n - i - 1, None, list(arr_copy)))

        self._sort_actions = actions
        if not actions:
            self._append_salida("La lista está vacía o no requiere ordenación.")
            return
        self._sorting = True
        self._set_controls_enabled(False)
        self.limpiar_salida()
        self._append_salida("Iniciando ordenación paso a paso (Bubble Sort)...")
        self._append_salida("-" * 40)
        self.after(200, self._perform_next_sort_action)

    def _perform_next_sort_action(self):
        if not self._sort_actions:
            self._sorting = False
            self._update_lista_display()
            self._append_salida("-" * 40)
            self._append_salida("Ordenación finalizada.")
            self.status_var.set("Lista ordenada (Bubble Sort).")
            self._set_controls_enabled(True)
            return

        action = self._sort_actions.pop(0)
        kind = action[0]
        if kind == 'compare':
            j, k, state = action[1], action[2], action[3]
            self._append_salida(f"Comparando índices {j} (val={state[j]}) y {k} (val={state[k]})")
            self._update_lista_display(highlight_indices=(j, k))
        elif kind == 'swap':
            j, k, state = action[1], action[2], action[3]
            self.lista = state
            self._append_salida(f"Intercambio: índice {j} <-> índice {k} -> nueva sublista: {self.lista}")
            self._update_lista_display(highlight_indices=(j, k))
        elif kind == 'pass_complete':
            idx = action[1]
            state = action[3]
            self.lista = state
            self._append_salida(f"Finalizado paso: posición {idx} fijada con valor {self.lista[idx]}")
            self._update_lista_display()
        else:
            self._append_salida(f"Acción desconocida: {action}")

        delay_ms = 200
        self.after(delay_ms, self._perform_next_sort_action)

    def _set_controls_enabled(self, enabled: bool):
        state = 'normal' if enabled else 'disabled'
        self.metodo_combo.config(state='readonly' if enabled else 'disabled')
        self.entry_valor.config(state=state)
        self._btn_ordenar.config(state=state)
        self._btn_gen.config(state=state)
        self._btn_buscar.config(state=state)
        self._btn_cargar.config(state=state)

    # -------------------------
    # Búsquedas
    # -------------------------
    def ejecutar_busqueda(self):
        if self._sorting:
            messagebox.showinfo("Ordenación en progreso", "Espera a que termine la ordenación antes de buscar.")
            return

        metodo = self.metodo_combo.get()
        valor_str = self.entry_valor.get().strip()

        if valor_str == "":
            messagebox.showwarning("Atención", "Introduce un valor entero para buscar.")
            return

        try:
            valor = int(valor_str)
        except:
            messagebox.showerror("Error", "Debes ingresar un número entero.")
            return

        self.limpiar_salida()
        self._append_salida(f"Método seleccionado: {metodo}")
        self._append_salida(f"Valor buscado: {valor}")
        self._append_salida("Lista: " + ", ".join(str(x) for x in self.lista))
        self._append_salida("-" * 40)

        def paso_cb(texto):
            self._append_salida(texto)

        if metodo == "Secuencial":
            idx = busqueda_secuencial(self.lista, valor, paso_cb)
            if idx != -1:
                self._append_salida(f"Resultado: encontrado en índice {idx}.")
                self.status_var.set(f"Encontrado en índice {idx}.")
            else:
                self._append_salida("Resultado: no encontrado.")
                self.status_var.set("Valor no encontrado.")

        elif metodo == "Binaria":
            if any(self.lista[i] > self.lista[i+1] for i in range(len(self.lista)-1)):
                respuesta = messagebox.askyesno("La lista no está ordenada",
                                                "La búsqueda binaria necesita lista ordenada. ¿Deseas ordenarla ahora?")
                if respuesta:
                    self.iniciar_ordenacion_paso()
                    return
                else:
                    self._append_salida("Aviso: la lista no está ordenada. Resultado puede ser incorrecto.")
            idx = busqueda_binaria(self.lista, valor, verbose_callback=paso_cb)
            if idx != -1:
                self._append_salida(f"Resultado: encontrado en índice {idx}.")
                self.status_var.set(f"Encontrado en índice {idx}.")
            else:
                self._append_salida("Resultado: no encontrado.")
                self.status_var.set("Valor no encontrado.")

        elif metodo == "Hash":
            indices = busqueda_hash(self.lista, valor, verbose_callback=paso_cb)
            if indices:
                self._append_salida(f"Resultado: encontrado en índice(s) {indices}.")
                self.status_var.set(f"Encontrado {len(indices)} ocurrencia(s).")
            else:
                self._append_salida("Resultado: no encontrado.")
                self.status_var.set("Valor no encontrado.")
        else:
            messagebox.showerror("Error", "Método desconocido.")


if __name__ == "__main__":
    app = BusquedasApp()
    app.mainloop()
