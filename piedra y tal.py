import tkinter as tk
from tkinter import messagebox
import random  # type: ignore
import oracledb
from PIL import Image, ImageTk

# ----- CREAR CONEXIÓN CON DB -----

def conectar_db():
    return oracledb.connect(
        user = "C##juego",
        password = "Holitas01",
        dsn = "localhost/xe"
    )

# ----- GUARDAR RESULTADOS EN ORACLE -----

def guardar_resultados(nombre, eleccion_jugador, eleccion_computador, gano):
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO resultados (nombre, eleccion_jugador, eleccion_computador, gano)
                       VALUES(:1,:2,:3,:4)
                       """, (nombre, eleccion_jugador, eleccion_computador, gano)) 
        conn.commit()
    except Exception as e:
        messagebox.showerror("Error de la base de datos,", str(e))
    finally:
        cursor.close()
        conn.close()

# Función para mostrar imagen (general para jugador y computadora)
def mostrar_imagen(label, eleccion):
    rutas_imagenes = {
        "Piedra": "T:/alternancia/jueves/piedra.png",
        "Papel": "T:/alternancia/jueves/papel.png",
        "Tijera": "T:/alternancia/jueves/tijera.png"
    }

    ruta = rutas_imagenes.get(eleccion)
    if ruta:
        imagen = Image.open(ruta).resize((100, 100))
        imagen_tk = ImageTk.PhotoImage(imagen)

        label.config(image=imagen_tk)
        label.image = imagen_tk

# Función principal del juego
def jugar(eleccion_jugador):
    opciones = ['Piedra', 'Papel', 'Tijera']
    eleccion_computadora = random.choice(opciones)

    resultado = ""
    gano = ""

    if eleccion_jugador == eleccion_computadora:
        resultado = "¡Empate!"
        gano = "No"
    elif (
        (eleccion_jugador == "Piedra" and eleccion_computadora == "Tijera") or
        (eleccion_jugador == "Papel" and eleccion_computadora == "Piedra") or
        (eleccion_jugador == "Tijera" and eleccion_computadora == "Papel")
    ):
        resultado = "¡Ganaste!"
        gano = "Si"
    else:
        resultado = "Perdiste."
        gano = "No"

    nombre = entry_nombre.get()
    if not nombre:
        messagebox.showerror("Error", "Debes ingresar tu nombre.")
        return

    # Mostrar resultado en ventana 
    mensaje = f"Jugador: {nombre}\nTu elección: {eleccion_jugador}\nComputadora: {eleccion_computadora}\nResultado: {resultado}"
    messagebox.showinfo("Resultado", mensaje)

    guardar_resultados(nombre, eleccion_jugador, eleccion_computadora, gano)
    print(f"[BD] Nombre: {nombre}, Elección: {eleccion_jugador}, ¿Ganó?: {gano}")

    # imagenes jugador y computadora
    mostrar_imagen(imagen_label_jugador, eleccion_jugador)
    mostrar_imagen(imagen_label_computadora, eleccion_computadora)

# ------- funcion del historial -------
def mostrar_jugadas():
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("SELECT id, nombre, eleccion_jugador, eleccion_computador, gano, FECHA FROM resultados")

        resultados = cursor.fetchall()

        cursor.close()
        conn.close()

        if not resultados:
            messagebox.showinfo("No hay jugadas registradas")
            return
            
        #ventana nueva
        ventana_lista = tk.Tk()
        ventana_lista.title("Historial de jugadas")
        ventana_lista.geometry("600x450")

        tk.Label(ventana_lista, text="ID | Nombre | eleccion_jugador | eleccion_computador | Gano | Fecha",font=("Arial", 10, "bold")).pack(pady=5)

        for fila in resultados:
            texto = f"({fila[0]} | {fila[1]} | {fila[2]} | {fila[3]} | {fila[4]} | {fila[5]})"
            tk.Label(ventana_lista, text=texto).pack()

    except oracledb.DatabaseError as e:
        messagebox.showerror("Error en BD", str(e))

# Interfaz
ventana = tk.Tk()
ventana.title("Piedra, Papel o Tijera")
ventana.geometry("400x480")  # un poco más alto para espacio

# ingresar nombre
tk.Label(ventana, text="Ingresa tu nombre:").pack(pady=5)
entry_nombre = tk.Entry(ventana)   
entry_nombre.pack()

# Botones de juego
tk.Label(ventana, text="Elige una opción:", font=("Arial", 12, "bold")).pack(pady=10)

btn_piedra = tk.Button(ventana, text="Piedra", width=15, command=lambda: jugar("Piedra"), 
                       bg="#C197C0", fg="white")
btn_piedra.pack(pady=5)

btn_papel = tk.Button(ventana, text="Papel", width=15, command=lambda: jugar("Papel"),
                      bg="#C43715")
btn_papel.pack(pady=5)

btn_tijera = tk.Button(ventana, text="Tijera", width=15, command=lambda: jugar("Tijera"),
                      bg="#BFC10B")
btn_tijera.pack(pady=5)

btn_historial = tk.Button(ventana, text="Historial de jugadas", width=15, command=mostrar_jugadas,
                       bg="#1A73E8")
btn_historial.pack(pady=15)

#mostrar elección jugador y computadora con imágenes
tk.Label(ventana, text="Tu elección:", font=("Arial", 10, "bold")).pack()
imagen_label_jugador = tk.Label(ventana)
imagen_label_jugador.pack(pady=(0, 15))

tk.Label(ventana, text="Computadora:", font=("Arial", 10, "bold")).pack()
imagen_label_computadora = tk.Label(ventana)
imagen_label_computadora.pack()

ventana.mainloop()