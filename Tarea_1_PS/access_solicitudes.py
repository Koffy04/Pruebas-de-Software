import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "tabla_solicitudes.csv")


field_solicitud = ['id','correo','id_equipo','fecha_inicial','fecha_final','estado_solicitud','estado_usuario']
convert_solicitud = {'C':'cancelado','F':'finalizado','P':'pendiente','A':'aprobado'}
convert_user = {'H': 'Habilitado', 'I': 'Inhabilitado'}
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
                            
                    elif sl_estadosol=="A":
                        print("Su solicitud ha sido aprobada, por lo que ya no se puede cancelar, puede ir a retirar el equipo...")
                    else:
                        print("Su solicitud se encuentra cancelada o fuera de plazo, consulte al encargado de turno para más información...")
                else:
                    print("No se encuentra una solicitud asociada a este correo.")
                    return