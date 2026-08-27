import csv
import os
from datetime import datetime, date, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "tabla_solicitudes.csv")

field_solicitud = ['id','correo','id_equipo','fecha_inicial','fecha_final','estado_solicitud','estado_usuario']
convert_solicitud = {'C':'cancelado','F':'finalizado','P':'pendiente','A':'aprobado'}
convert_user = {'H': 'Habilitado', 'I': 'Inhabilitado'}

def have_solicitud_correo(correo):

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        for row in reader:

            db_correo = row.get(field_solicitud[1])
            if db_correo == correo: # VER CASO DE FECHA PASADA
                return True
    
    return False

def have_solicitud_id_equipo(id):
    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for row in reader:
                db_id_equipo = row.get(field_solicitud[2])
                if db_id_equipo == id: # VER CASO DE FECHA PASADA
                    return True
                
    return False

def generar_solicitud(num_solicitud,correo_entregado,fecha_inicial,fecha_final):
    with open(DB_PATH, mode="r", encoding="utf-8") as escribir:
        writer = csv.DictWriter(escribir, fieldnames=field_solicitud)
        writer.writerow({'correo': correo_entregado, 'id_equipo': num_solicitud, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'estado_solicitud':'P'})
        return True

def resolver_solicitud():

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        print("| ID | Nombre del equipo | Estado del equipo |")
        # "ID | correo | id_equipo | fecha_inicial | fecha_final | estado_solicitud | estado_usuario"
        for row in reader:
            sl_correo = row.get(field_solicitud[1])
            sl_idsol = row.get(field_solicitud[2])
            sl_estadosol = row.get(field_solicitud[5])
            sl_fechai = row.get(field_solicitud[3])
            sl_fechaf = row.get(field_solicitud[4])
            # printeo de la información

    return

def estado_solicitud(correo):
    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            # "ID | correo | id_equipo | fecha_inicial | fecha_final | estado_solicitud | estado_usuario"
            for row in reader:
                sl_correo = row.get(field_solicitud[1])
                sl_idsol = row.get(field_solicitud[2])
                sl_estadosol = row.get(field_solicitud[5])
                sl_fechai = row.get(field_solicitud[3])
                sl_fechaf = row.get(field_solicitud[4])
                # printeo de la información
            if sl_correo==correo:
                if sl_estadosol=="P":
                    print("El estado de su solicitud es pendiente...")
                elif sl_estadosol=="A":
                    print("Su solicitud ha sido aprobada, puede ir a retirar el equipo...")
                elif sl_estadosol=="F":
                    print("Su solicitud ya no se encuentra vigente, realize otra solicitud...")
                else:
                    print("Su solicitud se encuentra cancelada, consulte al encargado de turno para más información...")
            else:
                print("No se encuentra una solicitud asociada a este correo.")
                return

def cancelar_solicitud(correo):
    with open(DB_PATH, mode="W", encoding="utf-8") as archivo:
                reader = csv.DictReader(archivo)
                # "ID | correo | id_equipo | fecha_inicial | fecha_final | estado_solicitud | estado_usuario"
                for row in reader:
                    sl_correo = row.get(field_solicitud[1])
                    sl_idsol = row.get(field_solicitud[2])
                    sl_estadosol = row.get(field_solicitud[5])
                    sl_fechai = row.get(field_solicitud[3])
                    sl_fechaf = row.get(field_solicitud[4])
                    # printeo de la información
                if sl_correo==correo:
                    if sl_estadosol=="P":
                        print("El estado de su solicitud es pendiente...")
                        print("----------------------\n")
                        print("¿Desea cancelarla? S=1; N=0")
                        print("----------------------\n")
                        resultado=input("")
                        if resultado:
                            print("") #ayuda dan falta por hacer este
                    elif sl_estadosol=="A":
                        print("Su solicitud ha sido aprobada, por lo que ya no se puede cancelar, puede ir a retirar el equipo...")
                    else:
                        print("Su solicitud se encuentra cancelada o fuera de plazo, consulte al encargado de turno para más información...")
                else:
                    print("No se encuentra una solicitud asociada a este correo.")
                    return

def solicitar_fecha_prestamo():
    hoy = date.today()
    fecha_minima = hoy + timedelta(days=3)

    while True:
        entrada = input("Ingrese la fecha de inicio del préstamo (DD/MM/AAAA): ")
        try:
            fecha_solicitada = datetime.strptime(entrada, "%d/%m/%Y").date()
        except ValueError:
            print("[Error] Formato inválido. Debe usar exactamente DD/MM/AAAA (ej. 15/04/2026).\n")
            continue

        if fecha_solicitada < hoy:
            print(f"[Error] No puede solicitar una fecha en el pasado. Hoy es {hoy.strftime('%d/%m/%Y')}.\n")
            continue
        if fecha_solicitada < fecha_minima:
            dias_diferencia = (fecha_solicitada - hoy).days
            print(
                f"[Error] Debe solicitar con al menos 3 días de anticipación. "
                f"La fecha más próxima permitida es {fecha_minima.strftime('%d/%m/%Y')} "
                f"(intentó solicitar con {dias_diferencia} día(s) de margen).\n"
            )
            continue
        print(f"[Éxito] Fecha aceptada: {fecha_solicitada.strftime('%d/%m/%Y')}")
        return fecha_solicitada

from datetime import datetime, date, timedelta

def solicitar_fecha_fin(fecha_inicio: date):
    # Límite máximo: hasta 7 días después de la fecha de inicio
    fecha_maxima = fecha_inicio + timedelta(days=7)

    while True:
        entrada = input(f"Ingrese la fecha de fin/devolución (DD/MM/AAAA) [Hasta {fecha_maxima.strftime('%d/%m/%Y')}]: ")
        try:
            fecha_fin = datetime.strptime(entrada, "%d/%m/%Y").date()
        except ValueError:
            print("[Error] Formato inválido. Debe usar exactamente DD/MM/AAAA.\n")
            continue
        if fecha_fin < fecha_inicio:
            print(f"[Error] La fecha de fin no puede ser anterior al inicio ({fecha_inicio.strftime('%d/%m/%Y')}).\n")
            continue

        if fecha_fin > fecha_maxima:
            duracion = (fecha_fin - fecha_inicio).days
            print(
                f"[Error] El préstamo no puede superar 1 semana (7 días). "
                f"Ingresó un período de {duracion} días.\n"
            )
            continue

        duracion_dias = (fecha_fin - fecha_inicio).days
        print(f"[Éxito] Préstamo configurado por {duracion_dias} día(s) (Hasta: {fecha_fin.strftime('%d/%m/%Y')}).")
        return fecha_fin