# ============================================================
#  bancoBackend.py  –  Servidor / Base de datos del banco
#  Estructuras usadas: Array (lista) + Cola (FIFO)
# ============================================================

# ESTRUCTURA #
class Cola:
    """Cola (First In, First Out)."""

    def __init__(self):
        self._datos = []

    def encolar(self, elemento):
        """Agrega un elemento al final de la cola."""
        self._datos.append(elemento)

    def estaVacia(self):
        return len(self._datos) == 0
    
    def desencolar(self):
        """Elimina y retorna el elemento más antiguo. Retorna None si está vacía."""
        if self.estaVacia():
            return None
        return self._datos.pop(0)

    def verFrente(self):
        """Consulta el frente sin eliminarlo."""
        return self._datos[0] if not self.estaVacia() else None

    def tamanio(self):
        return len(self._datos)

    def __repr__(self):
        return f"Cola{self._datos}"


# BASE DE DATOS (Array de usuarios) #
# Cada usuario: {"id": str, "pin": str, "nombre": str, "saldo": float}
usuarios = [
    {"id": "1001", "pin": "0000", "nombre": "Fhil User",  "saldo": 500_000.0},
    {"id": "1002", "pin": "1234", "nombre": "John Doe",   "saldo": 1_000_000.0},









]

# Cola global de transacciones pendientes de procesar
colaTransacciones = Cola()

# OPERACIONES SOBRE LA COLA #

def encolar_transaccion(transaccion):
    """Encola una transacción para procesamiento asíncrono."""
    colaTransacciones.encolar(transaccion)


def procesar_cola():
    """
    Procesa TODAS las transacciones pendientes en orden FIFO.
    Retorna lista de resultados.
    """
    resultados = []
    while not colaTransacciones.estaVacia():
        txn = colaTransacciones.desencolar()
        exito, mensaje = aplicarTransaccion(txn)
        resultados.append({"transaccion": txn, "exito": exito, "mensaje": mensaje})
    return resultados


def transacciones_pendientes():
    """Cantidad de transacciones en cola."""
    return colaTransacciones.tamanio()

# OPERACIONES SOBRE EL ARRAY DE USUARIOS #

def buscarUsuario(idCuenta):
    """Busca un usuario por ID en el array. Retorna el dict o None."""
    for usuario in usuarios:
        if usuario["id"] == idCuenta:
            return usuario
    return None


def validarPin(idCuenta, pin):
    """Valida credenciales. Retorna True si el PIN es correcto para la cuenta dada."""
    usuario = buscarUsuario(idCuenta)
    return usuario is not None and usuario["pin"] == pin


def consultarSaldo(idCuenta):
    """Retorna el saldo actual o None si la cuenta no existe."""
    usuario = buscarUsuario(idCuenta)
    return usuario["saldo"] if usuario else None


def aplicarTransaccion(transaccion):
    """
    Aplica una transacción al array de usuarios.
    transaccion = {"tipo": "retiro"|"deposito", "idCuenta": str, "monto": float}
    Retorna (exito: bool, mensaje: str).
    """
    usuario = buscarUsuario(transaccion["idCuenta"])
    if not usuario:
        return False, "Cuenta no encontrada."

    tipo  = transaccion["tipo"]
    monto = transaccion["monto"]

    if tipo == "retiro":
        if usuario["saldo"] < monto:
            return False, "Saldo insuficiente."
        usuario["saldo"] -= monto
        return True, f"Retiro de ${monto:,.0f} aplicado."

    elif tipo == "deposito":
        usuario["saldo"] += monto
        return True, f"Depósito de ${monto:,.0f} aplicado."

    return False, "Tipo de transacción desconocido."