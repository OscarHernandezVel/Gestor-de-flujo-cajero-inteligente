# Simulador de Cajero Automático (ATM) en Python

## Descripción
Este proyecto es una simulación de un entorno de cajero automático (ATM) desarrollado íntegramente en Python. Su objetivo principal es demostrar el manejo de flujos transaccionales separando la lógica en múltiples archivos y aplicando estructuras de datos fundamentales de la informática.

## Conceptos Aplicados
El proyecto implementa desde cero las siguientes estructuras de datos para gestionar la información:

* **Arrays (Listas):** Utilizados en el backend para simular la base de datos de usuarios registrados.
* **Pilas (LIFO - Last In, First Out):** Utilizadas en la sesión local del cajero para registrar el historial de transacciones del usuario. El último movimiento realizado es el primero en mostrarse.
* **Colas (FIFO - First In, First Out):** Utilizadas en el servidor del banco para encolar y procesar las transacciones de forma asíncrona, respetando estrictamente el orden de llegada.

## Estructura de Archivos



El proyecto está modularizado en 4 archivos principales:

| Archivo | Descripción |
| :--- | :--- |
| `receptorTransaccional.py` | Si el servidor central está lento, las transacciones se encolan para no perder ninguna solicitud del cliente |
| `procesadorTransaccional.py` | si una transferencia implica varios pasos y uno de estos falla, se usa una pila para deshacer los pasos en orden inverso
| `bancoBackend.py` | Simula el servidor de la entidad financiera. Contiene la "base de datos" en arrays y la cola de procesamiento. |
| `cajeroLogica.py` | Maneja la sesión del usuario actual, el registro del array del historial y las reglas de negocio del ATM (retiros, consultas, errores). |
| `main.py` | Punto de entrada de la aplicación. Ejecuta la interfaz de usuario en una ventana. |

## Requisitos
* Python 3.x instalado en tu sistema.
* No requiere librerías externas.

## Cómo Ejecutar el Proyecto
1. Clona o descarga este repositorio en tu máquina local.
2. Abre una terminal y navega hasta la carpeta del proyecto.
3. Ejecuta el archivo principal con el siguiente comando:
   ```bash
   python main.py
