# ============================================================
#  receptorTransaccional.py  –  Receptor de transacciones
#  Encola solicitudes cuando el servidor central está ocupado.
#  Estructura usada: Cola (FIFO) – sin perder ninguna solicitud
# ============================================================

import bancoBackend as banco


class ReceptorTransaccional:
    """
    Punto de entrada de transacciones externas (depósitos, retiros remotos).
    Usa la cola del backend para garantizar que ninguna solicitud se pierda
    aunque el servidor esté temporalmente lento.
    """

    def recibir(self, idCuenta, tipo, monto):
        """
        Valida y encola una transacción entrante.
        tipo: "retiro" | "deposito"
        Retorna (aceptada: bool, mensaje: str).
        """
        # Validaciones básicas antes de encolar
        if not banco.buscarUsuario(idCuenta):
            return False, f"Cuenta {idCuenta} no registrada."
        if monto <= 0:
            return False, "El monto debe ser mayor a cero."
        if tipo not in ("retiro", "deposito"):
            return False, f"Tipo '{tipo}' no reconocido."

        transaccion = {"tipo": tipo, "id_cuenta": idCuenta, "monto": monto}
        banco.encolar_transaccion(transaccion)

        pendientes = banco.transacciones_pendientes()
        return True, (
            f"Transacción aceptada y encolada. "
            f"Posición en cola: {pendientes}."
        )

    def procesar_pendientes(self):
        """
        Ordena al backend procesar todas las transacciones encoladas.
        Retorna la lista de resultados.
        """
        if banco.transacciones_pendientes() == 0:
            return []
        return banco.procesar_cola()

    def pendientes(self):
        """Cantidad de transacciones esperando en cola."""
        return banco.transacciones_pendientes()