# ============================================================
#  procesadorTransaccional.py  –  Procesador de transferencias
#  Usa una Pila para deshacer pasos en orden inverso (rollback)
#  si algún paso de la transferencia falla.
# ============================================================

import bancoBackend as banco


class ProcesadorTransaccional:
    """
    Ejecuta transferencias multi-paso entre cuentas.
    Cada paso completado se apila; si ocurre un fallo,
    se desapilan y revierten en orden LIFO (rollback).
    """

    def transferir(self, idOrigen, idDestino, monto):
        """
        Realiza una transferencia en dos pasos:
          1. Débito en cuenta origen.
          2. Crédito en cuenta destino.
        Si el paso 2 falla, el paso 1 se revierte automáticamente.
        Retorna (exito: bool, mensaje: str).
        """
        pila_pasos = []   # pila manual: lista donde el último elemento es la cima

        # ------ PASO 1: débito en origen ------
        banco.encolar_transaccion({"tipo": "retiro", "idCuenta": idOrigen, "monto": monto})
        resultados = banco.procesar_cola()
        res1 = resultados[0] if resultados else None

        if not res1 or not res1["exito"]:
            msg = res1["mensaje"] if res1 else "Error en débito."
            return False, f"Transferencia cancelada – Paso 1 fallido: {msg}"

        # Apilar el paso completado para posible rollback
        pila_pasos.append({"accion": "revertir retiro", "idCuenta": idOrigen, "monto": monto})

        # ------ PASO 2: crédito en destino ------
        if not banco.buscarUsuario(idDestino):
            # Cuenta destino no existe → rollback
            return False, self.rollback(pila_pasos, "Cuenta destino no existe.")

        banco.encolar_transaccion({"tipo": "deposito", "idCuenta": idDestino, "monto": monto})
        resultados = banco.procesar_cola()
        res2 = resultados[0] if resultados else None

        if not res2 or not res2["exito"]:
            return False, self.rollback(pila_pasos, res2["mensaje"] if res2 else "Error en crédito.")

        pila_pasos.append({"accion": "revertir deposito", "idCuenta": idDestino, "monto": monto})

        # Todos los pasos exitosos
        saldo_nuevo = banco.consultarSaldo(idOrigen)
        return True, (
            f"Transferencia de ${monto:,.0f} completada. "
            f"Saldo restante en origen: ${saldo_nuevo:,.0f}."
        )

    # ROLLBACK (desapila y revierte) #

    def rollback(self, pila_pasos, motivo):
        """
        Recorre la pila en orden LIFO y revierte cada paso aplicado.
        Retorna el mensaje de error final.
        """
        mensajes = [f"Rollback iniciado – motivo: {motivo}"]

        while pila_pasos:                       # desapilar hasta vaciar
            paso = pila_pasos.pop()             # cima → último paso ejecutado

            if paso["accion"] == "revertir retiro":
                # El débito ya se hizo → devolvemos el dinero
                banco.encolar_transaccion({
                    "tipo": "deposito",
                    "idCuenta": paso["idCuenta"],
                    "monto": paso["monto"]
                })
                banco.procesar_cola()
                mensajes.append(f"  ↩ Revertido débito de ${paso['monto']:,.0f} en cuenta {paso['idCuenta']}.")

            elif paso["accion"] == "revertir_deposito":
                # El crédito ya se hizo → lo quitamos
                banco.encolar_transaccion({
                    "tipo": "retiro",
                    "idCuenta": paso["idCuenta"],
                    "monto": paso["monto"]
                })
                banco.procesar_cola()
                mensajes.append(f"  ↩ Revertido crédito de ${paso['monto']:,.0f} en cuenta {paso['idCuenta']}.")

        return " | ".join(mensajes)