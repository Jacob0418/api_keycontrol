from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host="mysql-keycontrol.alwaysdata.net",
            user="352642",
            password="key_control2024",
            database="keycontrol_iotsm54"
        )
        return connection
    except Error as e:
        print(f"Error '{e}'")
    return None

@app.route('/salones', methods=['GET', 'POST'])
def manage_classroom():
    if request.method == 'POST':
        classroom_data = request.json
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO classroom (salon) VALUES (%s)", (classroom_data['salon'],))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Salon creado exitosamente"}, classroom_data), 201
    else:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM classroom")
        salones = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(salones)

@app.route('/tarjetas', methods=['GET', 'POST'])
def manage_cards():
    if request.method == 'POST':
        card_data = request.json
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()
            # Si es que el usuario existe en la base de datos
            cursor.execute("SELECT id FROM cards WHERE id = %s", (card_data['id'],))
            if cursor.fetchone() is None:
                return jsonify({"error": "Usuario no existe"}), 404
            
            # Si es que el usuario ya existe en la base de datos
            cursor.execute("INSERT INTO cards (uid, salon_id) VALUES (%s, %s)", (card_data['uid'], card_data['salon_id']))
            connection.commit()
            cursor.close()
            return jsonify({"message": "Tarjeta creada exitosamente"}, card_data), 201
    else:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cards")
        tarjetas = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(tarjetas)
        
@app.route('/grupos', methods=['GET', 'POST'])
def manage_groups():
    if request.method == 'POST':
        group_data = request.json
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO groups (grupo) VALUES (%s)", (group_data['grupo'],))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Grupo creado exitosamente"}, group_data), 201
    else:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM groups")
        grupos = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(grupos)
    
@app.route('/estudiantes', methods=['GET', 'POST'])
def manage_students():
    if request.method == 'POST':
        student_data = request.json
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()
            #Si no existe el grupo
            cursor.execute("SELECT id FROM students WHERE id = %s", (student_data['id'],))
            if cursor.fetchone() is None:
                return jsonify({"error": "Grupo no existe"}), 404
            
            #Si el grupo existe
            cursor.execute("INSERT INTO students (nombre, grupo_id) VALUES (%s, %s)", (student_data['nombre'], student_data['grupo_id']))
            connection.commit()
            cursor.close()
            return jsonify({"message": "Estudiante creado exitosamente"}, student_data), 201
        
# OBTENER DATOS POR ID

@app.route('/salones/<int:id>', methods=['GET'])
def get_classroom_by_id(id):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM classroom WHERE id = %s", (id,))
        usuario = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({"error": "Salón no encontrado"}), 404
    else:
        return jsonify({"error": "Error de conexión"}), 500
    
@app.route('/tarjetas/<int:id>', methods=['GET'])
def get_card_by_id(id):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cards WHERE id = %s", (id,))
        tarjeta = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if tarjeta:
            return jsonify(tarjeta), 200
        else:
            return jsonify({"error": "Tarjeta no encontrada"}), 404
    else:
        return jsonify({"error": "Error de conexión"}), 500
    
@app.route('/grupos/<int:id>', methods=['GET'])
def get_group_by_id(id):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM groups WHERE id = %s", (id,))
        grupo = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if grupo:
            return jsonify(grupo), 200
        else:
            return jsonify({"error": "Grupo no encontrado"}), 404
    else:
        return jsonify({"error": "Error de conexión"}), 500
    
@app.route('/estudiantes/<int:id>', methods=['GET'])
def get_student_by_id(id):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
        estudiante = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if estudiante:
            return jsonify(estudiante), 200
        else:
            return jsonify({"error": "Estudiante no encontrado"}), 404
    else:
        return jsonify({"error": "Error de conexión"}), 500

if __name__ == '__main__':
    app.run(debug=True)