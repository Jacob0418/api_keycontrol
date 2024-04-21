import asyncio
import websockets
import serial
import mysql.connector

# Función para crear la conexión a la base de datos
def create_db_connection():
    connection = mysql.connector.connect(
        host="mysql-keycontrol.alwaysdata.net",
        user="352642",
        password="key_control2024",
        database="keycontrol_iotsm54"
    )
    cursor = connection.cursor()
    return connection, cursor

# Función para leer tarjetas desde el lector serial
async def leer_tarjeta(ser, cursor, connection):
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

                # Insertar mensaje en la tabla access_control
                insert_query = "INSERT INTO access_control (information) VALUES (%s)"
                cursor.execute(insert_query, [uid])
                connection.commit()  # Hacer commit para guardar los cambios en la base de datos

                # Enviar comando 'N' al Arduino a través del puerto serial para abrir la puerta
                ser.write(b'N\n')
            else:
                mensaje = f"El UID {uid} no existe en la base de datos."
                await enviar_a_todos(mensaje)

# Lista de clientes WebSocket conectados
clientes_conectados = set()

# Función para manejar conexiones WebSocket
async def handler(websocket, path):
    clientes_conectados.add(websocket)
    try:
        async for message in websocket:  # Escuchar mensajes del cliente
            # Aquí puedes agregar la lógica para manejar diferentes comandos recibidos desde la aplicación móvil
            pass
    finally:
        clientes_conectados.remove(websocket)

# Función para enviar mensajes a todos los clientes WebSocket conectados
async def enviar_a_todos(mensaje):
    if clientes_conectados:  # Verificar si hay clientes conectados
        await asyncio.wait([cliente.send(mensaje) for cliente in clientes_conectados])

# Función principal
async def main():
    connection, cursor = create_db_connection()
    ser = serial.Serial('COM7', 9600)  # Ajusta el puerto y la velocidad según tu configuración
    await asyncio.gather(
        websockets.serve(handler, "localhost", 6789),
        leer_tarjeta(ser, cursor, connection)  # Pasar la conexión como argumento adicional
    )

# Iniciar el servidor WebSocket y la lectura del lector serial
asyncio.run(main())
