import websockets
import serial
import time
import asyncio
import mysql.connector

#CONFIGURAMOS LA BASE DE DATOS
def create_db_connection():
    connection = mysql.connector.connect(
        host="mysql-keycontrol.alwaysdata.net",
        user="352642",
        password="key_control2024",
        database="keycontrol_iotsm54"
        )

    cursor = connection.cursor()
    return connection, cursor

# Leer tarjeta del lector serial
async def leer_tarjeta(ser, cursor):
    while True:
        if ser.in_waiting > 0:
            uid = ser.readline().decode('utf-8').strip()
            print(f"UID de la tarjeta leído: {uid}")
            query = "SELECT * FROM cards WHERE uid = %s"
            cursor.execute(query, (uid,))
            resultados = cursor.fetchall()

            if resultados:
                mensaje = f"El UID {uid} existe en la base de datos.\n"
                for resultado in resultados:
                    mensaje += f"UID: {resultado[1]}, Otro dato: {resultado[2]}\n"
                await enviar_a_todos(mensaje)
            else:
                mensaje = f"El UID {uid} no existe en la base de datos."
                await enviar_a_todos(mensaje)
        await asyncio.sleep(0.1)

# Lista de clientes WebSocket conectados
clientes_conectados = set()

# Manejar conexiones WebSocket
async def handler(websocket, path):
    clientes_conectados.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clientes_conectados.remove(websocket)

# Enviar mensajes a todos los clientes WebSocket conectados
async def enviar_a_todos(mensaje):
    if clientes_conectados:  # Verificar si hay clientes conectados
        await asyncio.wait([cliente.send(mensaje) for cliente in clientes_conectados])

# Configuración inicial
async def main():
    connection, cursor = create_db_connection()
    ser = serial.Serial('COM7', 9600, timeout=1)
    task_leer_tarjeta = asyncio.create_task(leer_tarjeta(ser, cursor))
    start_server = websockets.serve(handler, "localhost", 6789)

    await asyncio.gather(start_server, task_leer_tarjeta)

# Iniciar el servidor WebSocket y la lectura del lector serial
asyncio.run(main())
