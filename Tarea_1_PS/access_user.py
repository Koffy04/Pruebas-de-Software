import csv
import re
import os

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
        correo = input("Ingresa tu correo (o '0' para volver): ")
        if correo == "0":
            return False
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

    check_status = False
    while not check_status:

        # Correo
        check_email = False
        pattern_email = re.compile(email_regex)

        while not check_email:  

            correo = input("Ingresa tu correo: ")
            if pattern_email.match(correo) :
                check_email = True

            else:
                print("\n< El correo no es válido >\n")

                
        # Contraseña
        check_password = False
        pattern_password = re.compile(password_regex)

        while not check_password:

            contrasena = input("Ingresa tu contraseña (Mínimo de 8 caracteres. Mínimo un número y una letra): ")

            if pattern_password.match(contrasena):

                c_contrasena = input("Vuelve a ingresar tu contraseña: ")
                 
                if contrasena == c_contrasena:
                    check_password = True

                else:
                    print("\n< Contraseñas no coinciden, vuelve a intentarlo >\n")
                            
            else:
                print("La contraseña no cumple con el mínimo de seguridad")

        check_status = register_check(nombre, correo, contrasena)

# Retorna el correo actual, después de un login
def get_correo():
    return correo

# Verifica si el usuario está habilitado para solicitar
def mostrar_usuarios():

    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:

        print("-" * 81)
        print(f"| {'Nombre':<25} | {'Correo':<30} | {'Estado':<15} |")
        print("-" * 81)

        reader = csv.DictReader(archivo)
        for row in reader:

            # Información bruta
            db_nombre = row.get(fieldnames[0])
            db_correo = row.get(fieldnames[1])
            db_tipo = row.get(fieldnames[3])
            db_estado = row.get(fieldnames[4])

            # printeo de la información
            if db_tipo == "solicitante":
                print(f"| {db_nombre:<25} | {db_correo:<30} | {convertion[db_estado]:<15} |")

        print("-" * 81)

# Ve el estado del solicitante basado en quién pregunta. En caso de ser encargado puede modificar el estado
def ver_estado_usuario(encargado):

    # Para Solicitante
    if not encargado:

        with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for row in reader:

                db_correo = row.get(fieldnames[1])
                db_estado = row.get(fieldnames[4])

                if db_correo == get_correo():

                    db_nombre = row.get(fieldnames[0])

                    if db_estado == "H":
                        
                        print(f"Solicitante {db_nombre} habilitado para solicitar equipos\n")
                        return True
                    
                    else:

                        print(f"Solicitante {db_nombre} Inhabilitado para pedir prestamo, porfavor resolver este problema con el encargado\n")
                        return False

    elif encargado:

        DONE = False
        while not DONE:

            mail = input("\n Excriba el correo del solicitante, que desee modificar su estado: ")

            with open(DB_PATH, mode="r", encoding="utf-8") as archivo:

                print("-" * 81)
                print(f"| {'Nombre':<25} | {'Correo':<30} | {'Estado':<15} |")
                print("-" * 81)

                found = False
                reader = csv.DictReader(archivo)
                for row in reader:

                    #información bruta
                    db_nombre = row.get(fieldnames[0])
                    db_correo = row.get(fieldnames[1])
                    db_estado = row.get(fieldnames[4])

                    if db_correo == mail:

                        found = True
                        print(f"| {db_nombre:<25} | {db_correo:<30} | {convertion[db_estado]:<15} |")
                        break

                print("-" * 81)

            if not found:
                print("\n< Correo no encontrado, pruebe con otro >\n")
                continue

            n_sure = input("\n¿Está seguro que quiere modificar este equipo? Y/N")
            if n_sure.upper() == "Y": DONE = True
            elif n_sure.upper() == "N": continue
            else: print("\n< Valor ingresado inválido. Ingrese de nuevo >\n")

        DONE = False
        while not DONE:

            estado = input("\nColoque el estado que le pondrá al solicitante (H: Habilitado, I: Inhabilitado)")
            if estado.upper() != "H" and estado.upper() != "I": 
                print("\n< Valor ingresado inválido. Ingrese de nuevo >\n")
            else:
                DONE = True
                cambiar_estado_usuario(mail,estado.upper())

# Cambia el estado del solicitante del correo objetivo
def cambiar_estado_usuario(mail,new_state):

    # Copia la información
    new_data = []
    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:

        reader = csv.DictReader(archivo)
        for row in reader:

            db_correo = row.get(fieldnames[1])
            if db_correo == mail:

                # Cambia el valor objetivo
                row[fieldnames[1]] = new_state

            new_data.append(row)

    # Restaura la información
    with open(DB_PATH, mode="w", newline='', encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_data)

    print("\n< Estado cambiado de forma exitosa >\n")
    return

# Verifica si la contraseña es correcta
def verificar_contrasena(passw):
    with open(DB_PATH, mode="r", encoding="utf-8") as archivo:
    
        reader = csv.DictReader(archivo)
        for row in reader:

            db_correo = row.get(fieldnames[1])
            db_contrasena = row.get(fieldnames[2])

            if db_correo == get_correo() and db_contrasena == passw:
                print("Contraseña verificada correctamente")
                return True

        return False