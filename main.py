import datetime
import re
import random
import json
from pymongo import MongoClient

# Clase de programa para generar archivo
def generate_report():
    try:
        # Entradas de usuario
        college_name = input("Introduce el nombre de la universidad: ")
        
        # Conexion mongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['unapec']
        empls_collection = db['payments']
        empls = list(empls_collection.find({'paid': True, 'college': college_name}))

        if not empls:
            print("No hay datos para procesar.")
            return

        # Creacion de diccionario de datos
        report = {}
        report["students"] = []

        # Calculadora de cuatrimestre
        current_month = datetime.datetime.now().month
        if current_month <= 4:
            term = "202301"
        elif 5 <= current_month <= 8:
            term = "202302"
        else:
            term = "202303"

        # Body
        total_amount = 0.0
        for emp in empls:
            student = {}
            student["name"] = emp["name"]
            student["id"] = emp["nationalId"]
            student["career"] = emp["career"]
            student["amount"] = float(emp["amount"])
            student["date"] = datetime.datetime.now().strftime('%Y-%m-%d')
            student["credits"] = emp["credits"]
            student["term"] = term

            total_amount += emp["amount"]
            report["students"].append(student)

        # Generando el total de montos y el numero de referencia
        report["totalAmount"] = round(total_amount, 2)
        report["referenceNumber"] = str(random.randint(100000000, 999999999))

        # Escribir el JSON
        with open('report.json', 'w') as f:
            json.dump(report, f, indent=4)

        print("Archivo generado de forma satisfactoria.")
    
    except Exception as e:
        print(f"Ha ocurrido un error: {str(e)}")

# Clase de programa para importar archivo
def process_input_file():
    filepath = input("Introduce la ruta del archivo: ").strip()

    # Conexion mongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['unapec']
    input_payms_collection = db['input_payms_json']

    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            for student in data['students']:
                input_payms_collection.insert_one(student)

        print("Archivo procesado correctamente.")
    except Exception as e:
        print(f"Error procesando el archivo: {str(e)}")

# Menu
def show_menu():
    while True:
        print("\nEscoge una opción:")
        print("1. Exportar archivo de nómina.")
        print("2. Importar archivo de nómina.")
        print("3. Salir")

        user_choice = input("Opción elegida: ")
        if user_choice == '1':
            generate_report()
        elif user_choice == '2':
            process_input_file()
        elif user_choice == '3':
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida, por favor digita una opción del menú.")

# Mostrar menu cuando corre el programa
show_menu()