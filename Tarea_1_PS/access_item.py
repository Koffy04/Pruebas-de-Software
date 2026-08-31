import csv
import os
import access_solicitudes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "tabla_equipos.csv")

fieldnames = ['id', 'nombre_equipo', 'descripcion', 'estado']
convertion = {'ME': 'Mal estado', 'BE': 'Buen estado'}

# Muestra la información del equipo dependiendo de quién pregunte
def mostrar_equipos(encargado):

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:

        # Para Encargado
        if encargado:

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

        # Para solicitante
        elif not encargado:

            reader = csv.DictReader(archivo)
            print("| ID | Nombre del equipo | Descripción del equipo ")
            for row in reader:

                db_estado = row.get(fieldnames[3])
                if db_estado == "BE":

                    db_id = row.get(fieldnames[0])
                    if not access_solicitudes.have_solicitud_id_equipo(db_id):

                        db_nombre = row.get(fieldnames[1])
                        db_descripcion = row.get(fieldnames[2])

                        # printeo de la información
                        print(f"| {db_id} | {db_nombre} | {db_descripcion} |")
        
    return

# Ve el estado de los equipos. Se puede modificar el estado 
def ver_estado_equipo():

    DONE = False
    while not DONE:

        id = input("\n Escriba el ID del equipo, que desee modificar su estado: ")

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

                    found = True
                    print(f"\n| {db_id} | {db_nombre} | {convertion[db_estado]} |")     
                    break

        if not found:
            print("\n< ID no encontrado, puebe con otro >")
            continue

        n_sure = input("\n¿Está seguro que quiere modificar este equipo? Y/N")
        if n_sure.upper() == "Y": DONE = True
        elif n_sure.upper() == "N": continue
        else: print("\n< Valor ingresado inválido. Ingrese de nuevo >\n")

    DONE = False
    while not DONE:

        estado = input("\nColoque el estado que le pondrá al equipo (ME: Mal estado, BE: Buen estado)")
        if estado.upper() != "ME" and estado.upper() != "BE": 
            print("\n< Valor ingresado inválido. Ingrese de nuevo >\n") 
        else:
            DONE = True
            cambiar_estado_equipo(id, estado.upper())

# Cambia el estado del equipo del ID objetivo
def cambiar_estado_equipo(id,new_state):

    # Copia la información
    new_data = []
    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
        
        reader = csv.DictReader(archivo)
        for row in reader:

            db_id = row.get(fieldnames[0])
            if db_id == id:

                # Cambia el valor objetivo
                row[fieldnames[0]] = new_state

            new_data.append(row)

    # Restaura la información
    with open(DB_PATH, mode="w", newline='', encoding="utf-8") as archivo:
            
            writer = csv.DictWriter(archivo, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(new_data)

    print("\n< Estado cambiado de forma exitosa >\n")
    return


def confirmar_equipo(id):

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:

        reader = csv.DictReader(archivo)
        for row in reader:

            bd_id = row.get(fieldnames[0])
            bd_estado = row.get(fieldnames[3])

            if bd_id == id and bd_estado == 'BE':
                return True
            
        return False