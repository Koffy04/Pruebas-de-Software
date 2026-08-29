import csv
import re
import os
import access_solicitudes

email_regex = r"(?:[a-z0-9!#$%&'*+\x2f=?^_`\x7b-\x7d~\x2d]+(?:\.[a-z0-9!#$%&'*+\x2f=?^_`\x7b-\x7d~\x2d]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9\x2d]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9\x2d]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9\x2d]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
password_regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "tabla_usuarios.csv")

fieldnames = ['nombre', 'correo', 'contraseña', 'tipo', 'estado']
convertion = {'H': 'Habilitado', 'I': 'Inhabilitado'}

correo = ""

# Verifica si existe el usuario en la tabla
def login_check(email, passw):
    global correo

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
                    correo = email
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
        print("\n< ¡¡Usuario registrado exitosamente!! >\n")
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
            print("\n< Valor ingresado inválido. Ingrese de nuevo >\n")

    # Correo
    check_email = False
    pattern_email = re.compile(email_regex)
    while not check_email:
        correo = input("Ingresa tu correo: ")
        if pattern_email.match(correo):
            check_email = True
        else:
            print("\n< El correo no es válido >\n")

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
            print("\n< Contraseñas no coinciden, vuelve a intentarlo >\n")
            check_password = False
    
    return

def have_solicitudes():
    return access_solicitudes.have_solicitud_correo(correo)

def estado_usuario():

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:

        reader = csv.DictReader(archivo)
        for row in reader:
            
            db_correo = row.get(fieldnames[1])
            db_estado = row.get(fieldnames[4])

            if db_correo == correo and db_estado == "H":
                print("\n< Usuario habilitado para solicitar equipos >\n")
                return True
            
        print("Su usuario se encuentra Inhabilitado para pedir prestamo, porfavor resolver este problema con el encargado\n")
        return False

def get_correo():
    return correo


def cambiar_estado_usuario(correo: str, nuevo_estado: str = None):
    if not os.path.exists(DB_PATH):
        print(f"\n[Error] No se encontró el archivo: {DB_PATH}")
        return

    nuevo_estado = nuevo_estado.upper() if nuevo_estado else None
    if nuevo_estado and nuevo_estado not in convertion:
        print("\n[Error] Estado inválido. Solo se permite 'H' o 'I'.")
        return

    filas = []
    usuario_encontrado = False
    datos_usuario = None

    # 1. Leer el archivo y actualizar el estado en memoria
    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        for row in reader:
            db_correo = row.get("correo", "").strip()

            if db_correo == correo.strip():
                usuario_encontrado = True
                estado_actual = row.get("estado", "").strip().upper()

                # Si no se pasó nuevo_estado, se invierte: H -> I / I -> H
                if not nuevo_estado:
                    estado_destino = "I" if estado_actual == "H" else "H"
                else:
                    estado_destino = nuevo_estado

                row["estado"] = estado_destino
                datos_usuario = row

            filas.append(row)

    if not usuario_encontrado:
        print(f"\n[Error] No se encontró ningún usuario con el correo: {correo}")
        return

    # 2. Guardar los cambios en el CSV
    with open(DB_PATH, mode="w", newline='', encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filas)

    # 3. Mostrar confirmación en pantalla
    print("\n< Estado de usuario actualizado de forma exitosa >")
    print("-" * 65)
    print(f"| {'Nombre':<18} | {'Correo':<22} | {'Rol':<12} | {'Estado':<12} |")
    print("-" * 65)
    print(
        f"| {datos_usuario['nombre']:<18} "
        f"| {datos_usuario['correo']:<22} "
        f"| {datos_usuario['tipo']:<12} "
        f"| {convertion.get(datos_usuario['estado'], datos_usuario['estado']):<12} |"
    )
    print("-" * 65 + "\n")