import csv
import os
import access_user
import access_item
import fecha
from datetime import date, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "tabla_solicitudes.csv")

TARIFA_MORA_DIARIA = 2000 

field_solicitud = ['id','correo','id_equipo','fecha_inicial','fecha_final','estado_solicitud']
convert_solicitud = {'C':'cancelado','F':'finalizado','P':'pendiente','A':'aprobado', 'R':'rechazado', 'D':'deuda'}

field_user = ['nombre', 'correo', 'contraseña', 'tipo', 'estado']
convert_user = {'H': 'Habilitado', 'I': 'Inhabilitado'}

# verifica si el correo tiene asociado una solicitud activa
def have_solicitud_correo():

    correo = access_user.get_correo()
    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:

        reader = csv.DictReader(archivo)
        for row in reader:

            db_correo = row.get(field_solicitud[1])
            db_estado = row.get(field_solicitud[5])

            if db_correo == correo and (db_estado == 'A' or db_estado == 'P' or db_estado=='D'): 
                return True
        else:
            print("Usted ya posee una solicitud en espera, Cumpla con la solicitud o cancelela")
            return False

# Verifica si el ID del equipo tiene una solicitud activa
def have_solicitud_id_equipo(id):

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
            
            reader = csv.DictReader(archivo)
            for row in reader:
                
                db_id_equipo = row.get(field_solicitud[2])
                if db_id_equipo == id:
                    return True
                
    return False

# Solicita la fecha de inicio de la solicitud
def solicitar_fecha_inicial():

    print(f"Hoy es {fecha.get_actual()}, La fecha mínima de solicitud es {fecha.plus_bussiness_3days()}")

    while True:

        date = input("Ingrese la fecha de inicio del préstamo (DD/MM/AAAA): ")
        if fecha.compare_date_past(date):
            print("Fecha inicial registarda exitosamente\n")
            break

        else:
            print("Intentelo de nuevo\n")

    return date

# Solicita la fecha de término de la solicitud
def solicitar_fecha_final(date):
    print(f"Tienes 1 semana (7 días) para devolver")

    while True:

        fecha.show_week(date)

        f_date = input("Ingrese la fecha de devolución (DD/MM/AAAA): ")
        if fecha.compare_date_future(f_date):
            print("Fecha final registarda exitosamente\n")
            break

        else:
            print("Intentelo de nuevo\n")

# Ingresa la solicitud al sistemas
def solicitar_equipo():

    # Solicitar ID de equipo
    print("\n¿Qué equipo desea solicitar? Ingrese el ID correspondiente\n")
    id = input("Su respuesta: ")

    while True:

        # Checkear ID de equipo válido
        if access_item.confirmar_equipo(id) and have_solicitud_id_equipo(id):
            break
            
        print("\n< Por favor ingrese un ID válido> \n")
        print("\n¿Qué equipo desea solicitar? Ingrese el ID correspondiente\n")
        id = input("Su respuesta: ")

    # Solicitar fecha del préstamo
    DONE = False
    while not DONE:

        fecha_inicial = solicitar_fecha_inicial()
        fecha_final = solicitar_fecha_final(fecha_inicial)

        n_sure = input(f"\n¿Está seguro que quiere escoger este rango de fechas (desde {fecha_inicial} hasta {fecha_final})? Y/N").upper()
        if n_sure == "Y": DONE = True
        elif n_sure == "N": continue
        else: print("\n< Valor ingresado inválido. Ingrese de nuevo >\n")

    print("Fechas del préstamo asignados correctamente, generando solicitud...\n")

    # Generar la solicitud
    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:

        reader = csv.reader(archivo,delimiter = ",")
        data = list(reader)
        row_count = len(data)
    
    with open(DB_PATH, mode="a", newline='', encoding="utf-8") as archivo:

        writer = csv.DictWriter(archivo, fieldnames=field_solicitud)
        writer.writerow({'id': row_count,
                          'correo': access_user.get_correo(),
                          'id_equipo': id,
                          'fecha_inicial': fecha_inicial,
                          'fecha_final': fecha_final,
                          'estado_solicitud':'P'
                          })
        print("Solicitud válida, generando Solicitud para su próxima aprobación/rechazo")
        return True

    print("Algo fallo con la solicitud, intentelo denuevo.")
    return False

# Ve todas las solicitudes y sus estados
def mostrar_solicitudes(encargado):

    if not encargado:

        # Para solicitante
        with open(DB_PATH, mode="r", encoding="utf-8") as archivo:

            count = 0
            print("| N° de solicitud | ID del equipo | Fecha de inicio | Fecha de término | Estado |")

            reader = csv.DictReader(archivo)
            for row in reader:

                # Datos brutos
                db_correo = row.get(field_solicitud[1])
                db_iditem = row.get(field_solicitud[2])
                db_fechai = row.get(field_solicitud[3])
                db_fechaf = row.get(field_solicitud[4])
                db_estado = row.get(field_solicitud[5])

                if db_correo == access_user.get_correo():
                    count += 1
                    print(f"| {count} | {db_iditem} | {db_fechai} | {db_fechaf} | {convert_solicitud[db_estado]}")

            if count == 0:
                print("No se encuentra ninguna solicitud asocioda a este correo.")
                return
            
    elif encargado:

        # Para encargado
        with open(DB_PATH, mode="r", encoding="utf-8") as archivo:

            print("| ID solicitud | Correo de usuario | ID del equipo | Fecha de inicio | Fecha de término | Estado |")

            reader = csv.DictReader(archivo)
            for row in reader:

                # Información bruta
                db_id = row.get(field_solicitud[0])
                db_correo = row.get(field_solicitud[1])
                db_iditem = row.get(field_solicitud[2])
                db_fechai = row.get(field_solicitud[3])
                db_fechaf = row.get(field_solicitud[4])
                db_estado = row.get(field_solicitud[5])

                # printeo de la información
                print(f"| {db_id} | {db_correo} | {db_iditem} | {db_fechai} | {db_fechaf} | {convert_solicitud[db_estado]} |")

    return

# Cancela una solicitud actual
def cancelar_solicitud():

    new_data = []
    found = False

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:

        reader = csv.DictReader(archivo)
        for row in reader:

            db_correo = row.get(field_solicitud[1])
            db_fechaf = row.get(field_solicitud[4])
            db_estado = row.get(field_solicitud[5])

            if db_correo == access_user.get_correo():
                if fecha.commpare_simple(db_fechaf):
                    found = True
                    if db_estado == "P":
                        while True:
                            n_sure = input("Su solicitud está a la espera de ser aprobada ¿Está seguro que quiere cancelarla? Y/N").upper()
                            if n_sure == "Y":

                                passw = input("Ingrese su contraseña para confirmar: ")
                                if access_user.verificar_contrasena(passw):
  
                                    row[field_solicitud[5]] = "C"
                                    break

                                else:
                                    print("Contraseña incorrecta intentando de nuevo")

                            elif n_sure == "N":

                                print("Saliendo de la operación...")
                                return

                            else:
                                print("\n< Valor ingresado inválido. Ingrese de nuevo >\n")

                    elif db_estado == "A": print("Su solicitud se encuentra aprobada, por lo que no se puede cancelar")
                    elif db_estado == "R": print("Su solicitud se encuentra rechazada, por lo que no se puede cancelar")
                    elif db_estado == "C": print("Su solicitud ya se encuentra cancelada")

            new_data.append(row)

    if not found:

        print("\nNo se encuentra una solicitud actual asociada a este correo.")
        return
    
    with open(DB_PATH, mode="w", encoding="utf-8", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=field_solicitud)
        writer.writeheader()
        writer.writerows(new_data)


def calcular_deuda_demora(fecha_fin_pactada: date, fecha_entrega_real: date, tarifa_por_dia) -> dict:
    if fecha_entrega_real <= fecha_fin_pactada:
        return {
            "dias_atraso": 0,
            "monto_deuda": 0,
            "estado": "A tiempo"
        }
    dias_atraso = (fecha_entrega_real - fecha_fin_pactada).days
    total_deuda = dias_atraso * tarifa_por_dia

    return {
        "dias_atraso": dias_atraso,
        "monto_deuda": total_deuda,
        "estado": "Con atraso"
    }


def calcular_deuda_demora_usuario(tarifa_diaria) -> dict:

    correo_usuario = access_user.get_correo()
    hoy = fecha.get_actual()
    deuda_total = 0
    dias_totales_atraso = 0
    solicitudes_con_atraso = []

    if not os.path.exists(DB_PATH):
        return {
            "estado": "error",
            "mensaje": f"No se encontró el archivo: {DB_PATH}",
            "deuda_total": 0,
            "dias_atraso": 0,
            "detalles": []
        }

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
        lector_csv = csv.DictReader(archivo)
        
        for fila in lector_csv:
            correo = fila["correo"].strip()
            estado = fila["estado_solicitud"].strip().upper()
            if correo == correo_usuario and estado == "D":
                try:
                    fecha_limite = datetime.strptime(fila["fecha_final"].strip(), "%Y-%m-%d").date()
                except ValueError:
                    continue  

                calculo = calcular_deuda_demora(fecha_limite, hoy, tarifa_diaria)
                
                if calculo["dias_atraso"] > 0:
                    dias_totales_atraso += calculo["dias_atraso"]
                    deuda_total += calculo["monto_deuda"]
                    
                    solicitudes_con_atraso.append({
                        "id_solicitud": fila["id"].strip(),
                        "id_equipo": fila["id_equipo"].strip(),
                        "fecha_final": str(fecha_limite),
                        "dias_atraso": calculo["dias_atraso"],
                        "monto": calculo["monto_deuda"]
                    })

    return {
        "estado": "ok",
        "correo": correo_usuario,
        "deuda_total": deuda_total,
        "dias_atraso": dias_totales_atraso,
        "detalles": solicitudes_con_atraso
    }

# Muestra solamente las solicitudes pendientes
def mostrar_pendientes():

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:

        print("| ID solicitud | Correo de usuario | ID del equipo | Fecha de inicio | Fecha de término | Estado |")

        reader = csv.DictReader(archivo)
        for row in reader:

            # Información bruta
            db_id = row.get(field_solicitud[0])
            db_correo = row.get(field_solicitud[1])
            db_iditem = row.get(field_solicitud[2])
            db_fechai = row.get(field_solicitud[3])
            db_fechaf = row.get(field_solicitud[4])
            db_estado = row.get(field_solicitud[5])

            # printeo de la información
            if db_estado == "P":
                print(f"| {db_id} | {db_correo} | {db_iditem} | {db_fechai} | {db_fechaf} | {convert_solicitud[db_estado]} |")

    return

# Rechaza o aprueba una solicitud objetivo
def resolver_solicitud():

    new_data = []
    found = False

    id = input("Ingrese el ID de la solicitud que desea cambiar")

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
    
        reader = csv.DictReader(archivo)
        for row in reader:

            # Información bruta
            db_id = row.get(field_solicitud[0])
            db_correo = row.get(field_solicitud[1])
            db_iditem = row.get(field_solicitud[2])
            db_fechai = row.get(field_solicitud[3])
            db_fechaf = row.get(field_solicitud[4])
            db_estado = row.get(field_solicitud[5])

            if db_id == id and db_estado == "P":
            
                found = True

                n_sure = input(f"¿Está seguro que quiere ver esta solicitud [{db_id} | {db_correo} | {db_iditem} | {db_fechai} | {db_fechaf} | {db_estado}] ? Y/N").upper()
                if n_sure == "Y":
                    while True:

                        print("\nSeleccione el nuevo estado para esta solicitud:")
                        print(" [A] Aprobado")
                        print(" [R] Rechazado")
                        print(" [0] Cancelar operación sin cambios")
                        new_state = input("\nSu respuesta: ").upper()
                        
                        if new_state == "0":

                            print("\nOperación cancelada. Saliendo de la operación...")
                            return
                        
                        elif new_state == 'A' or new_state == 'R':

                            row[field_solicitud[5]] = new_state
                            print(f"Solicitud {convert_solicitud[new_state]} exitosamente")
                            break

                        else:
                            print("[Error] Opción no válida. Ingrese una de las letras indicadas.")

                elif n_sure == "N":
                    print("Saliendo de la operación por seguridad de los datos")
                    return
                    
            new_data.append(row)

    if not found:
        print("\nNo se encuentra una solicitud actual asociada al ID.")
        return

    with open(DB_PATH, mode="w", encoding="utf-8", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=field_solicitud)
        writer.writeheader()
        writer.writerows(new_data)