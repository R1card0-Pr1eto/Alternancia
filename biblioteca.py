import tkinter as tk
from tkinter import messagebox
import oracledb

def conexion():
    conn = oracledb.connect(
        user ="C##biblioteca",
        password = "Holitas01",
        dsn = "localhost/xe"
    )
    cursor = conn.cursor()
    return conn, cursor

#funcion ingreso de datos

def insertar_biblioteca():
    try:
        id_bib = int(entry_id.get())
        nombre = entry_nombre.get()
        municipalidad = entry_municipalidad.get()

        if not nombre or not municipalidad:
            messagebox.showerror("Error","Todos los campos son obligatorios")
            return
        
        conn, cursor = conexion()
        
        cursor.execute("""
                       INSERT INTO biblioteca (id_biblioteca,nombre,municipalidad)
                       VALUES (:1, :2, :3)
                       """,(id_bib,nombre,municipalidad))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Exito","Biblioteca registrada Exitosamente")
        entry_id.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_municipalidad.delete(0, tk.END)

    except oracledb.DatabaseError as e:
        messagebox.showerror("Error en DB", str(e))
    except ValueError:
        messagebox.showerror("Error","El ID debe ser un numero")

def mostrar_biblioteca():
    try:
        conn, cursor = conexion()
        cursor.execute("SELECT id_biblioteca, Nombre, Municipalidad FROM biblioteca")
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not resultado:
            messagebox.showinfo("Biblioteca","No hay Bibliotecas registradas")
            return
        
            #crear nueva ventana
        ventana_lista = tk.Tk()
        ventana_lista.title("Lista de Biblioteca")
        ventana_lista.geometry("500x400")

        tk.Label(ventana_lista, text= "ID |Nombre | Municipalidad",
             font=("Arial", 10, "bold")).pack(pady=5)
        
        for fila in resultado:
            texto= f"({fila[0]} | {fila[1]} | {fila[2]})"
            tk.Label(ventana_lista, text=texto).pack()

    except oracledb.DatabaseError as e:
        messagebox.showerror("Error en BD", str(e))


ventana = tk.Tk()
ventana.title("Registro de Biblioteca")
ventana.geometry("700x500")

#etiquetas y campos
tk.Label(ventana, text="ID Biblioteca").pack(pady=5)
entry_id = tk.Entry(ventana)
entry_id.pack()

tk.Label(ventana, text="Nombre:").pack(pady=5)
entry_nombre = tk.Entry(ventana)
entry_nombre.pack()

tk.Label(ventana, text="Municipalidad:").pack(pady=5)
entry_municipalidad = tk.Entry(ventana)
entry_municipalidad.pack()

#boton insertar
tk.Button(ventana, text="Registrar Biblioteca", command= insertar_biblioteca).pack(pady=15)
#boton mostrar
tk.Button(ventana, text="Mostrar Biblioteca", command= mostrar_biblioteca).pack(pady=35)

ventana.mainloop()