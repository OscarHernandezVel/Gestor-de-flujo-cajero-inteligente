# ============================================================
#  cajeroLogica.py  –  Lógica de sesión del cajero
#  Estructuras usadas: Pila (LIFO) para historial de sesión
# ============================================================

import bancoBackend as banco

# ESTRUCTURA #
class Pila:
    """Pila (Last In, First Out)."""

    def __init__(self):
        self.datos = []

    def apilar(self, elemento):
        """Agrega un elemento a la cima."""
        self.datos.append(elemento)

    def desapilar(self):
        """Elimina y retorna el elemento de la cima. Retorna None si está vacía."""
        if self.estaVacia():
            return None
        return self.datos.pop()

    def estaVacia(self):
        return len(self.datos) == 0
    
    def verCima(self):
        """Consulta la cima sin eliminarla."""
        return self.datos[-1] if not self.estaVacia() else None

    def tamanio(self):
        return len(self.datos)

    def todos(self):
        """Retorna todos los elementos (el último es la cima)."""
        return list(self.datos)

    def __repr__(self):
        return f"Pila{self.datos}"


# SESIÓN DEL CAJERO #

class SesionCajero:
    """
    Maneja la sesión activa de un usuario.
    Registra cada operación en una Pila.
    """

    MAX_RETIROS_SESION = 3          # límite de retiros por sesión
    MONTO_MAX_RETIRO   = 1_000_000  # límite por operación

    def __init__(self, idCuenta):
        self.idCuenta       = idCuenta
        self.activa          = True
        self.historial      = Pila()   # pila de movimientos de la sesión
        self.retirosCount  = 0

#  HISTORIAL (PILA) #

    def registrar(self, tipo, monto, detalle):
        """Apila un nuevo movimiento en el historial de sesión."""
        entrada = {"tipo": tipo, "monto": monto, "detalle": detalle}
        self.historial.apilar(entrada)

    def ver_ultimo_movimiento(self):
        """Retorna la cima de la pila (último movimiento)."""
        return self.historial.verCima()

    def ver_historial_completo(self):
        """
        Retorna todos los movimientos en orden LIFO
        (el más reciente primero).
        """
        return list(reversed(self.historial.todos()))
    
# OPERACIONES #

    def consultarSaldo(self):
        """Consulta saldo en el backend y registra en historial."""
        saldo = banco.consultarSaldo(self.idCuenta)
        self.registrar("CONSULTA", 0, f"Saldo disponible: ${saldo:,.0f}")
        return saldo

    def retirar(self, monto):
        """
        Encola un retiro en el backend.
        Valida límites antes de encolar.
        Retorna (exito: bool, mensaje: str).
        """
        if monto <= 0:
            return False, "El monto debe ser mayor a cero."
        if monto > self.MONTO_MAX_RETIRO:
            return False, f"Monto máximo por retiro: ${self.MONTO_MAX_RETIRO:,.0f}."
        if self.retirosCount >= self.MAX_RETIROS_SESION:
            return False, "Límite de retiros por sesión alcanzado."

        saldoActual = banco.consultarSaldo(self.idCuenta)
        if saldoActual < monto:
            self.registrar("RETIRO_FALLIDO", monto, "Saldo insuficiente.")
            return False, "Saldo insuficiente."

        # Encolar en el banco
        banco.encolar_transaccion({
            "tipo": "retiro",
            "idCuenta": self.idCuenta,
            "monto": monto
        })
        # Procesar inmediatamente (modo síncrono del cajero)
        resultados = banco.procesar_cola()
        resultado  = resultados[0] if resultados else None

        if resultado and resultado["exito"]:
            self.retirosCount += 1
            self.registrar("RETIRO", monto, f"Exitoso – nuevo saldo: ${banco.consultarSaldo(self.idCuenta):,.0f}")
            return True, f"Retiro de ${monto:,.0f} realizado con éxito."
        else:
            msg = resultado["mensaje"] if resultado else "Error desconocido."
            self.registrar("RETIRO_FALLIDO", monto, msg)
            return False, msg

    def cerrarSesion(self):
        """Cierra la sesión activa."""
        self.activa = False
        self.registrar("CIERRE", 0, "Sesión cerrada por el usuario.")