import csv
import os
import access_user
from datetime import datetime, date, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "tabla_solicitudes.csv")
TARIFA_MORA_DIARIA = 2000 
field_solicitud = ['id','correo','id_equipo','fecha_inicial','fecha_final','estado_solicitud','estado_usuario']
convert_solicitud = {'C':'cancelado','F':'finalizado','P':'pendiente','A':'aprobado', 'D':'deuda'}
convert_user = {'H': 'Habilitado', 'I': 'Inhabilitado'}

def have_solicitud_correo(correo):

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        for row in reader:

            db_correo = row.get(field_solicitud[1])
            db_estado =row.get(field_solicitud[5])
            if db_correo == correo and (db_estado == 'A' or db_estado == 'P' or db_estado=='D'): 
                return True
            else:
                return False

def have_solicitud_id_equipo(id):
    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for row in reader:
                db_id_equipo = row.get(field_solicitud[2])
                if db_id_equipo == id: # VER CASO DE FECHA PASADA
                    return True
                
    return False

def generar_solicitud(num_solicitud,fecha_inicial,fecha_final):
    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
        reader = csv.reader(archivo,delimiter = ",")
        data = list(reader)
        row_count = len(data)
    
    with open(DB_PATH, mode="a", newline='', encoding="utf-8") as escribir:
        writer = csv.DictWriter(escribir, fieldnames=field_solicitud)
        writer.writerow({'id': row_count, 'correo': access_user.get_correo(), 'id_equipo': num_solicitud, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'estado_solicitud':'P'})
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
    filas = []
    encontrada = False
    modificada = False

    # 1. Leer todas las filas del CSV
    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        fieldnames = reader.fieldnames
        for row in reader:
            sl_correo = row.get("correo")
            sl_estadosol = row.get("estado_solicitud")

            if sl_correo == correo:
                encontrada = True
                if sl_estadosol == "P":
                    print("El estado de su solicitud es pendiente...")
                    print("----------------------\n")
                    print("¿Desea cancelarla? S=1; N=0")
                    print("----------------------\n")
                    resultado = input("Seleccione una opción: ").strip()

                    if resultado == "1":
                        row["estado_solicitud"] = "C"
                        modificada = True
                        print("\n[Éxito] Solicitud cancelada correctamente.")
                    else:
                        print("\nOperación abortada. La solicitud sigue pendiente.")
                elif sl_estadosol == "A":
                    print("\nSu solicitud ha sido aprobada, por lo que ya no se puede cancelar, puede ir a retirar el equipo...")
                elif sl_estadosol == "C":
                    print("\nSu solicitud ya se encuentra cancelada.")
                else:
                    print("\nSu solicitud se encuentra fuera de plazo o inactiva, consulte al encargado de turno.")

            filas.append(row)
    if not encontrada:
        print("\nNo se encuentra una solicitud asociada a este correo.")
        return
    if modificada:
        with open(DB_PATH, mode="w", encoding="utf-8", newline="") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filas)

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

def solicitar_fecha_fin(fecha_inicio: date):
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
#Esto es pa probar .3.
def calcular_deuda_demora(fecha_fin_pactada: date, fecha_entrega_real: date, tarifa_por_dia: int = TARIFA_MORA_DIARIA) -> dict:
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

# 2. Función de consulta en CSV
def calcular_deuda_demora_usuario(correo_usuario: str, tarifa_diaria: int = TARIFA_MORA_DIARIA) -> dict:
    hoy = date.today()
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

            # Solo evaluamos las solicitudes activas / con posible mora
            # Ajusta las letras a tus estados (e.g., 'D' o 'P')
            if correo == correo_usuario and estado == "D":
                try:
                    fecha_limite = datetime.strptime(fila["fecha_final"].strip(), "%Y-%m-%d").date()
                except ValueError:
                    continue  

                # Reutilizamos la función de cálculo matemático
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