import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "tabla_equipos.csv")

fieldnames = ['id', 'nombre_equipo', 'descripcion', 'estado']
convertion = {'ME': 'Mal estado', 'BE': 'Buen estado'}

def mostrar_equipos():

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        print("| ID | Nombre del equipo | Descripción del equipo | Estado del equipo |")
        for row in reader:

            # Información bruta
            db_id = row.get(fieldnames[0])
            db_nombre = row.get(fieldnames[1])
            db_descripcion = row.get(fieldnames[2])
            db_estado = row.get(fieldnames[3])

            # printeo de la información
            print(f"| {db_id} | {db_nombre} | {db_descripcion} | {convertion[db_estado]} |")
        
    return

def mostrar_estados():

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        print("| ID | Nombre del equipo | Estado del equipo |")
        for row in reader:

            # Información bruta
            db_id = row.get(fieldnames[0])
            db_nombre = row.get(fieldnames[1])
            db_estado = row.get(fieldnames[3])

            # printeo de la información
            print(f"| {db_id} | {db_nombre} | {convertion[db_estado]} |")

    return

def mostrar_estado_individual():

    done = False
    while not done:

        id = input("\n Escriba el ID del equipo, que desee modificar el estado: ")

        with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
            found = False
            reader = csv.DictReader(archivo)
            print("| ID | Nombre del equipo | Estado del equipo |")
            for row in reader:

                # Información bruta
                db_id = row.get(fieldnames[0])
                db_nombre = row.get(fieldnames[1])
                db_estado = row.get(fieldnames[3])

                if db_id == id:
                    # printeo de la información
                    print(f"\n| {db_id} | {db_nombre} | {convertion[db_estado]} |")
                    found = True

            if not found:
                print("\n<ID no encontrado, puebe con otro>")
                continue

        n_sure = input("\n¿Está seguro que quiere modificar este equipo? Y/N")
        if n_sure.upper() == "Y":
            done = True
        elif n_sure.upper() == "N":
            continue
        else:
            print("\n<Valor ingresado inválido. Ingrese de nuevo>\n")

    done = False
    while not done:

        estado = input("\nColoque el estado que le pondrá al equipo (ME: Mal estado, BE: Buen estado)")
        if estado != "ME" and estado != "BE":
            print("\n<Valor ingresado inválido. Ingrese de nuevo>\n")
        else:
            cambiar_estado(id, estado)


def cambiar_estado(id,new_state):

    # Copiar toda la información de la tabla
    new_data = []
    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
        
        reader = csv.DictReader(archivo)
        for row in reader:

            # Cambiar el valor de la fila especificada
            db_id = row.get(fieldnames[0])
            if db_id == id:
                row[fieldnames[0]] = new_state

            new_data.append(row)

    # Restaura la información
    with open(DB_PATH, mode="w", newline='', encoding="utf-8") as archivo:
            
            writer = csv.DictWriter(archivo, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(new_data)

    print("Estado cambiado de forma exitosa")
    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:

        reader = csv.DictReader(archivo)
        print("| ID | Nombre del equipo | Estado del equipo |")
        for row in reader:

            # Información bruta
            db_id = row.get(fieldnames[0])
            db_nombre = row.get(fieldnames[1])
            db_estado = row.get(fieldnames[3])

            if db_id == id:
                # printeo de la información
                print(f"\n| {db_id} | {db_nombre} | {convertion[db_estado]} |")
                found = True

    return