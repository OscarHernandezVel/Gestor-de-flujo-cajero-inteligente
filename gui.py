import tkinter as tk
from tkinter import messagebox, simpledialog
import cajeroLogica as cajero
import procesadorTransaccional as procesador
import main as receptor

class CajeroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cajero Automatico")
        self.root.geometry("400x300")
        self.sesion = None
        self.receptor = receptor.ReceptorTransaccional()
        self.procesador = procesador.ProcesadorTransaccional()

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Bienvenido al Cajero Automatico", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="ID de Cuenta:").pack()
        self.id_entry = tk.Entry(self.root)
        self.id_entry.pack()

        tk.Label(self.root, text="PIN:").pack()
        self.pin_entry = tk.Entry(self.root, show="*")
        self.pin_entry.pack()

        tk.Button(self.root, text="Iniciar Sesion", command=self.login).pack(pady=10)

    def login(self):
        id_cuenta = self.id_entry.get()
        pin = self.pin_entry.get()

        if not id_cuenta or not pin:
            messagebox.showerror("Error", "Por favor ingrese ID y PIN.")
            return

        import bancoBackend as banco
        if banco.validarPin(id_cuenta, pin):
            self.sesion = cajero.SesionCajero(id_cuenta)
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "ID o PIN incorrecto.")

    def create_main_screen(self):
        self.clear_screen()

        tk.Label(self.root, text=f"Cuenta: {self.sesion.idCuenta}", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Consultar Saldo", command=self.consultar_saldo).pack(fill=tk.X, padx=20, pady=5)
        tk.Button(self.root, text="Retirar Dinero", command=self.retirar).pack(fill=tk.X, padx=20, pady=5)
        tk.Button(self.root, text="Depositar Dinero", command=self.depositar).pack(fill=tk.X, padx=20, pady=5)
        tk.Button(self.root, text="Transferir", command=self.transferir).pack(fill=tk.X, padx=20, pady=5)
        tk.Button(self.root, text="Ver Historial", command=self.ver_historial).pack(fill=tk.X, padx=20, pady=5)
        tk.Button(self.root, text="Cerrar Sesion", command=self.cerrar_sesion).pack(fill=tk.X, padx=20, pady=5)

    def consultar_saldo(self):
        saldo = self.sesion.consultarSaldo()
        messagebox.showinfo("Saldo", f"Saldo disponible: ${saldo:,.0f}")

    def retirar(self):
        monto = simpledialog.askfloat("Retirar", "Ingrese el monto a retirar:")
        if monto is not None:
            exito, mensaje = self.sesion.retirar(monto)
            messagebox.showinfo("Resultado", mensaje)

    def depositar(self):
        monto = simpledialog.askfloat("Depositar", "Ingrese el monto a depositar:")
        if monto is not None:
            exito, mensaje = self.receptor.recibir(self.sesion.idCuenta, "deposito", monto)
            if exito:
                self.receptor.procesar_pendientes()
                messagebox.showinfo("Resultado", "Deposito realizado con exito.")
            else:
                messagebox.showerror("Error", mensaje)

    def transferir(self):
        id_destino = simpledialog.askstring("Transferir", "Ingrese ID de cuenta destino:")
        if id_destino:
            monto = simpledialog.askfloat("Transferir", "Ingrese el monto a transferir:")
            if monto is not None:
                exito, mensaje = self.procesador.transferir(self.sesion.idCuenta, id_destino, monto)
                messagebox.showinfo("Resultado", mensaje)

    def ver_historial(self):
        historial = self.sesion.ver_historial_completo()
        if not historial:
            messagebox.showinfo("Historial", "No hay movimientos en esta sesion.")
        else:
            hist_text = "\n".join([f"{m['tipo']}: {m['detalle']}" for m in historial])
            messagebox.showinfo("Historial", hist_text)

    def cerrar_sesion(self):
        self.sesion.cerrarSesion()
        self.sesion = None
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CajeroGUI(root)
    root.mainloop()