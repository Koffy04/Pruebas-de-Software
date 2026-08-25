import csv
import re
import os

email_regex = r"(?:[a-z0-9!#$%&'*+\x2f=?^_`\x7b-\x7d~\x2d]+(?:\.[a-z0-9!#$%&'*+\x2f=?^_`\x7b-\x7d~\x2d]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9\x2d]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9\x2d]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9\x2d]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
password_regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "tabla_usuarios.csv")

fieldnames = ['nombre', 'correo', 'contraseña', 'tipo', 'estado']
convertion = {'H': 'Habilitado', 'I': 'Inhabilitado'}
#######
DB_PATH_EQ = os.path.join(BASE_DIR, "db", "tabla_equipos.csv")
field_item = ['id', 'nombre_equipo', 'descripcion', 'estado']
convert_item = {'ME': 'Mal estado', 'BE': 'Buen estado'}
#######
DB_PATH_SO = os.path.join(BASE_DIR, "db", "tabla_solicitudes.csv")
field_solicitud = ['id','correo','id_equipo','fecha_inicial','fecha_final','estado_solicitud','estado_usuario']
convert_solicitud = {'C':'cancelado','F':'finalizado','P':'pendiente','A':'aprobado'}
#######
# Verifica si existe el usuario en la tabla

def login_check(email, passw):

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        for row in reader:

            db_nombre = row.get(fieldnames[0])
            db_correo = row.get(fieldnames[1])
            db_contrasena = row.get(fieldnames[2])
            db_tipo = row.get(fieldnames[3])

            # Verificación si existe correo en BD
            if db_correo == email:

                #Verificación si existe contraseña en BD
                if db_contrasena == passw:
                    print("Usuario encontrado")
                    if db_tipo == "encargado":
                        print(f"Bienvenido Encargado {db_nombre}")
                        return True,True
                    else:
                        print(f"Bienvenido Solicitante {db_nombre}")
                        return True,False
                        
                else:
                    print("Contraseña incorrecta")
                    return False,False

        print("No existe un correo asociado a la cuenta")
        return False,False

# Registra un nuevo usuario en la tabla, si no existe
def register_check(name, email, passw):

    # Verificación si existe correo en BD
    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        for row in reader:
            if row.get('correo') == email:
                print("El email de usuario ya se encuentra registrado.")
                return False

    # Registra el usuario
    with open(DB_PATH, mode="a", newline='', encoding="utf-8") as archivo:
        
        writer = csv.DictWriter(archivo, fieldnames=fieldnames)
        writer.writerow({'nombre': name, 'correo': email, 'contraseña': passw, 'tipo': 'solicitante', 'estado': 'H'})
        print("\n<¡¡Usuario registrado exitosamente!!>\n")
        return True

# Inicio de sesión
def login():
    check_status = False
    while not check_status:

        # Solicitamos los datos
        correo = input("Ingresa tu correo: ")
        contrasena = input("Ingresa tu contraseña: ")

        # Con los datos, erificamos la existencia del usuario
        check_status,encargado = login_check(correo, contrasena)

    # Importante para la diferenciación de la interfaz
    if encargado:
        return True
    else:
        return False

# Registro de usuario
def register():

    # Nombre
    check_name = False
    while not check_name:
        nombre = input("Ingresa tu nombre y apellido, siguiendo el Siguiente formato 'Nombre Apellido': ")
        n_sure = input(f"¿Estás seguro que '{nombre}' está bien escrito? Y/N: ")
        if n_sure.upper() == "Y":
            check_name = True
        elif n_sure.upper() == "N":
            continue
        else:
            print("\n<Valor ingresado inválido. Ingrese de nuevo>\n")

    # Correo
    check_email = False
    pattern_email = re.compile(email_regex)
    while not check_email:
        correo = input("Ingresa tu correo: ")
        if pattern_email.match(correo):
            check_email = True
        else:
            print("\n<El correo no es válido>\n")

    # Contraseña
    check_status = False
    check_password = False
    pattern_password = re.compile(password_regex)
    while not check_status:
        while not check_password:
            contrasena = input("Ingresa tu contraseña (Mínimo de 8 caracteres. Mínimo un número y una letra): ")
            if pattern_password.match(contrasena):
                check_password = True
            else:
                print("La contraseña no cumple con el mínimo de seguridad")

        c_contrasena = input("Vuelve a ingresar tu contraseña: ")
        if contrasena == c_contrasena:
            check_status = register_check(nombre, correo, contrasena)
        else:
            print("\n<Contraseñas no coinciden, vuelve a intentarlo\n>")
            check_password = False
    
    return

def confirmar_tabla_equipos(num_solicitud):
    with open(DB_PATH_EQ, mode="r", encoding="utf-8") as lectura:
        for row in lectura:
            id = row.get(field_item[0])
            nombre = row.get(field_item[1])
            desc = row.get(field_item[2])
            estado = row.get(field_item[3])
            if id == num_solicitud:
                if estado == 'BE':
                    return True
                else:
                    print("El equipo no está en un buen estado para ser prestado")
            else:
                print("El equipo no existe en la base de datos")
                return False

def estado_usuario(correo_entregado):
    with open(DB_PATH, mode="r", encoding="utf-8") as lectura:
        for row in lectura:
            db_nombre = row.get(fieldnames[0])
            db_correo = row.get(fieldnames[1])
            db_contrasena = row.get(fieldnames[2])
            db_tipo = row.get(fieldnames[3])
            if  db_correo== correo_entregado:
                if db_tipo=="H":
                    return True
                else:
                    print("Su usuario se encuentra Inhabilitado para pedir prestamo, porfavor resolver este problema con el encargado de turno\n")
                    return False
            else:
                print("El correo entregado no coincide con nuestra base de datos\n")
                return False

def generar_solicitud(num_solicitud,correo_entregado,fecha_inicial,fecha_final):
    with open(DB_PATH_SO, mode="r", encoding="utf-8") as escribir:
        writer = csv.DictWriter(escribir, fieldnames=field_solicitud)
        writer.writerow({'correo': correo_entregado, 'id_equipo': num_solicitud, 'fecha_inicial': fecha_inicial, 'fecha_final': fecha_final, 'estado_solicitud':'P'})
        return True