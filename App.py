import tkinter as tk
from tkinter import messagebox
import re
import random

# Clase de Usuario
class Usuario:
    def __init__(self, nombre, correo, telefono, contrasena):
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.contrasena = contrasena

# Clase de Bicicleta
class Bicicleta:
    def __init__(self, modelo, estado, ubicacion, precio):
        self.modelo = modelo
        self.estado = estado
        self.ubicacion = ubicacion
        self.precio = precio

    def marcar_como_alquilada(self):
        if self.estado == 'disponible':
            self.estado = 'alquilada'

# Clase de Reserva
class Reserva:
    def __init__(self, usuario, bicicletas_disponibles):
        self.usuario = usuario
        self.bicicletas_disponibles = bicicletas_disponibles
        self.bicicleta_seleccionada = None
        self.fecha_inicio = None
        self.hora_inicio = None
        self.horas_alquiladas = None

    def seleccionar_bicicleta(self, index):
        if index >= 0 and index < len(self.bicicletas_disponibles):
            bicicleta = self.bicicletas_disponibles[index]
            if bicicleta.estado == 'disponible':
                self.bicicleta_seleccionada = bicicleta
                self.bicicleta_seleccionada.estado = 'reservada'
                return True
        return False

    def pagar_y_confirmar(self, monto, horas_alquiladas):
        if self.bicicleta_seleccionada and self.bicicleta_seleccionada.estado == 'reservada':
            self.horas_alquiladas = horas_alquiladas
            return random.randint(1000, 9999)  # Número de confirmación único

# Clase para la lógica de reserva de bicicletas y su interfaz
class ReservaGUI:
    def __init__(self, root, usuarios, bicicletas):
        self.root = root
        self.usuarios = usuarios
        self.bicicletas = bicicletas
        self.nombre_entry = None
        self.reserva = None

    def mostrar_seleccion_bicicleta(self):
        self.limpiar_pantalla()

        bicicletas_label = tk.Label(self.root, text="Bicicletas Disponibles")
        bicicletas_label.pack()

        for i, bicicleta in enumerate(self.bicicletas):
            # Crea una cadena con la información de la bicicleta
            info_bicicleta = f"Modelo: {bicicleta.modelo}\nDisponibilidad: {bicicleta.estado}\nUbicación: {bicicleta.ubicacion}\nPrecio: ${bicicleta.precio}"
            # Crea el botón con la información de la bicicleta
            bicicleta_button = tk.Button(self.root, text=info_bicicleta, command=lambda b=bicicleta, i=i: self.seleccionar_bicicleta(b, i))
            bicicleta_button.pack()

    def mostrar_seleccion_fecha_hora(self):
        fecha_label = tk.Label(self.root, text="Fecha de inicio (YYYY-MM-DD):")
        fecha_label.pack()

        fecha_entry = tk.Entry(self.root)
        fecha_entry.pack()

        hora_label = tk.Label(self.root, text="Hora de inicio (HH:MM):")
        hora_label.pack()

        hora_entry = tk.Entry(self.root)
        hora_entry.pack()

        continuar_button = tk.Button(self.root, text="Continuar", command=lambda: self.pedir_horas(fecha_entry.get(), hora_entry.get()))
        continuar_button.pack()

    def pedir_horas(self, fecha, hora):
        if not fecha or not hora:
            messagebox.showerror("Error", "¡Error! Debes ingresar fecha y hora de inicio válidas.")
            return

        while not re.match(r'\d{4}-\d{2}-\d{2}', fecha):
                messagebox.showerror("Error", "El formato de fecha no es válido. Debe ser YYYY-MM-DD.")
                fecha = input("Ingresa la fecha de inicio (YYYY-MM-DD): ")

        self.reserva.fecha_inicio = fecha
        self.reserva.hora_inicio = hora

        horas_label = tk.Label(self.root, text="Número de horas de alquiler:")
        horas_label.pack()

        horas_entry = tk.Entry(self.root)
        horas_entry.pack()

        continuar_button = tk.Button(self.root, text="Continuar",
                                    command=lambda: self.pagar_confirmar(horas_entry.get()))
        continuar_button.pack()


    def seleccionar_bicicleta(self, bicicleta, index):
        if bicicleta.estado == 'disponible':
            nombre_usuario = self.nombre_entry.get()
            if not nombre_usuario:
                messagebox.showerror("Error", "¡Error! Debes ingresar tu nombre de usuario.")
                return

            self.reserva = Reserva(self.usuarios[nombre_usuario], self.bicicletas)
            if self.reserva.seleccionar_bicicleta(index):
                self.mostrar_seleccion_fecha_hora()

    def pagar_confirmar(self, horas):
        if not horas or not horas.isdigit():
            messagebox.showerror("Error", "¡Error! Debes ingresar un número válido de horas de alquiler.")
            return

        horas_alquiladas = int(horas)
        precio_total = self.reserva.bicicleta_seleccionada.precio * horas_alquiladas

        monto_label = tk.Label(self.root, text=f"Monto a pagar: ${precio_total}")
        monto_label.pack()

        monto_entry = tk.Entry(self.root)
        monto_entry.pack()

        pagar_button = tk.Button(self.root, text="Pagar",
                                command=lambda: self.confirmar_reserva(monto_entry.get(), horas_alquiladas))
        pagar_button.pack()

    def confirmar_reserva(self, monto, horas_alquiladas):
        if not monto or not monto.isdigit():
            messagebox.showerror("Error", "¡Error! Debes ingresar un monto válido.")
            return

        monto_ingresado = int(monto)
        if monto_ingresado < self.reserva.bicicleta_seleccionada.precio * horas_alquiladas:
            messagebox.showerror("Error", "¡Error! El monto ingresado es insuficiente.")
            return

        numero_confirmacion = self.reserva.pagar_y_confirmar(monto_ingresado, horas_alquiladas)
        if numero_confirmacion:
            mensaje_confirmacion = (
                f"Nombre del cliente: {self.reserva.usuario.nombre}\n"
                f"Tipo de bicicleta alquilada: {self.reserva.bicicleta_seleccionada.modelo}\n"
                f"Ubicación de la bicicleta: {self.reserva.bicicleta_seleccionada.ubicacion}\n"
                f"Horas alquiladas: {horas_alquiladas}\n"
                f"Precio: ${monto_ingresado}\n"
                f"Número de orden de confirmación único: {numero_confirmacion}"
            )
            messagebox.showinfo("Reserva Confirmada", mensaje_confirmacion)
        else:
            messagebox.showerror("Error", "¡Error! La reserva no pudo ser confirmada.")

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

# Clase de la Interfaz de Usuario
class InterfazUsuario:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Usuario")
        self.root.geometry("400x300")
        self.usuarios = {}  # Almacena los usuarios registrados
        self.bicicletas = [Bicicleta("GW", "disponible", "Universidad de Medellín", 10),
                          Bicicleta("Scott", "disponible", "Eafit", 15),
                          Bicicleta("Trek", "disponible", "UPB", 20)]
        self.reserva_gui = None  # Instancia de ReservaGUI

        self.nombre_label = tk.Label(self.root, text="Nombre:")
        self.nombre_label.pack()

        self.nombre_entry = tk.Entry(self.root)
        self.nombre_entry.pack()

        self.correo_label = tk.Label(self.root, text="Correo Electrónico:")
        self.correo_label.pack()

        self.correo_entry = tk.Entry(self.root)
        self.correo_entry.pack()

        self.telefono_label = tk.Label(self.root, text="Teléfono:")
        self.telefono_label.pack()

        self.telefono_entry = tk.Entry(self.root)
        self.telefono_entry.pack()

        self.contrasena_label = tk.Label(self.root, text="Contraseña:")
        self.contrasena_label.pack()

        self.contrasena_entry = tk.Entry(self.root, show="*")
        self.contrasena_entry.pack()

        self.registrar_button = tk.Button(self.root, text="Registrar", command=self.registrar_usuario)
        self.registrar_button.pack()

    def validar_correo(self, correo):
        return "@" in correo and "." in correo

    def validar_telefono(self, telefono):
        return len(telefono) >= 10

    def registrar_usuario(self):
        nombre = self.nombre_entry.get()
        correo = self.correo_entry.get()
        telefono = self.telefono_entry.get()
        contrasena = self.contrasena_entry.get()

        if not nombre or not correo or not telefono or not contrasena:
            messagebox.showerror("Error", "¡Error! Todos los campos son obligatorios.")
        elif len(nombre) < 3:
            messagebox.showerror("Error", "¡Error! El nombre debe tener al menos 3 caracteres.")
        elif not self.validar_correo(correo):
            messagebox.showerror("Error", "¡Error! El correo electrónico no es válido.")
        elif not self.validar_telefono(telefono):
            messagebox.showerror("Error", "¡Error! El número de teléfono debe tener al menos 10 dígitos.")
        else:
            # Guardar los datos del usuario en un diccionario
            self.usuarios[nombre] = Usuario(nombre, correo, telefono, contrasena)
            messagebox.showinfo("Registro Exitoso", "¡Registro exitoso!")

            # Muestra la sección de bicicletas disponibles y opción de cambiar contraseña
            self.mostrar_seccion_bicicletas()
            self.cambiar_contrasena_button = tk.Button(self.root, text="Cambiar Contraseña", command=self.cambiar_contrasena)
            self.cambiar_contrasena_button.pack()

    def cambiar_contrasena(self):
        self.limpiar_pantalla()

        nombre_label = tk.Label(self.root, text="Nombre de Usuario:")
        nombre_label.pack()

        nombre_entry = tk.Entry(self.root)
        nombre_entry.pack()

        contrasena_actual_label = tk.Label(self.root, text="Contraseña Actual:")
        contrasena_actual_label.pack()

        contrasena_actual_entry = tk.Entry(self.root, show="*")
        contrasena_actual_entry.pack()

        nueva_contrasena_label = tk.Label(self.root, text="Nueva Contraseña:")
        nueva_contrasena_label.pack()

        nueva_contrasena_entry = tk.Entry(self.root, show="*")
        nueva_contrasena_entry.pack()

        cambiar_button = tk.Button(self.root, text="Cambiar Contraseña",
                                   command=lambda: self.cambiar_contrasena_confirmacion(nombre_entry.get(),
                                                                                     contrasena_actual_entry.get(),
                                                                                     nueva_contrasena_entry.get()))
        cambiar_button.pack()

    def cambiar_contrasena_confirmacion(self, nombre, contrasena_actual, nueva_contrasena):

        if nombre in self.usuarios and contrasena_actual == self.usuarios[nombre].contrasena:
            self.usuarios[nombre].contrasena = nueva_contrasena
            messagebox.showinfo("Cambio de Contraseña", "¡Contraseña cambiada con éxito!")
            # Después de cambiar la contraseña, muestra la sección de bicicletas disponibles
            self.mostrar_seccion_bicicletas()
        else:
            messagebox.showerror("Error", "¡Error! Nombre de usuario o contraseña actual incorrectos.")



    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def mostrar_seccion_bicicletas(self):
        self.limpiar_pantalla()
        self.nombre_entry.config(state="readonly")  # Bloquea la entrada del nombre de usuario
        self.reserva_gui = ReservaGUI(self.root, self.usuarios, self.bicicletas)
        self.reserva_gui.nombre_entry = self.nombre_entry  # Pasa el nombre_entry a la instancia
        self.reserva_gui.mostrar_seleccion_bicicleta()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazUsuario(root)
    root.mainloop()
