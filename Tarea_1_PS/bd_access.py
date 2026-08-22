import csv
import re

email_regex = "(?:[a-z0-9!#$%&'*+\x2f=?^_`\x7b-\x7d~\x2d]+(?:\.[a-z0-9!#$%&'*+\x2f=?^_`\x7b-\x7d~\x2d]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9\x2d]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9\x2d]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9\x2d]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
password_regex = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

# Verifica si existe el usuario en la tabla
def login_check(email, passw):

    with open("db/tabla_usuarios.csv", mode="r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        for row in reader:

            # Verificación si existe correo en BD
            if row.get('correo') == email:

                #Verificación si existe contraseña en BD
                if row.get('contraseña') == passw:
                    print("Usuario encontrado")
                    print(f"Bienvenido {row['nombre']}")
                    return True
                else:
                    print("Contraseña incorrecta")
                    return False
            else:
                print("No existe un correo asociado a la cuenta")
                return False

# Registra un nuevo usuario en la tabla, si no existe
def register_check(name, email, passw):

    # Verificación si existe correo en BD
    with open("db/tabla_usuarios.csv", mode="r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        for row in reader:
            if row.get('correo') == email:
                print("El email de usuario ya se encuentra registrado.")
                return False

    # Registra el usuario
    with open("db/tabla_usuarios.csv", mode="a", newline="", encoding="utf-8") as archivo:
        fieldnames = ['nombre', 'correo', 'contraseña']
        writer = csv.DictWriter(archivo, fieldnames=fieldnames)
            
        # Escribimos el nuevo usuario
        writer.writerow({'nombre': name, 'correo': email, 'contraseña': passw})
        print("Usuario registrado exitosamente.")
        return True
       

# Inicio de sesión
def login():
    check_status = False
    while not check_status:
        correo = input("Ingresa tu correo: ")
        contrasena = input("Ingresa tu contraseña: ")
        check_status = login_check(correo, contrasena)
    return

# Reistro de usuario
def register():
    # Nombre
    check_name = False
    while not check_name:
        nombre = input("Ingresa tu nombre y apellido: ")
        n_sure = input(f"¿Estás seguro que {nombre} es tu nombre? Y/N: ")
        if n_sure.upper() == "Y":
            check_name = True

    # Correo
    check_email = False
    pattern_email = re.compile(email_regex)
    while not check_email:
        correo = input("Ingresa tu correo: ")
        if pattern_email.match(correo):
            check_email = True
        else:
            print("El correo no es válido")

    # Conraseña
    check_status = False
    check_password = False
    pattern_password = re.compile(password_regex)
    while not check_status:
        while not check_password:
            contrasena = input("Ingresa tu contraseña (Mínimo de 8 caracteres. Mínimo un número y una letra): ")
            if pattern_password.match(contrasena):
                check_password = True
            else:
                print("La contraseña no cumple con em mínimo de seguridad")

        c_contrasena = input("Vuelve a ingresar tu contraseña: ")
        if contrasena == c_contrasena:
            check_status = register_check(nombre, correo, contrasena)
        else:
            print("Contraseñas no coinciden, vuelve a intentarlo")
            check_password = False
    
    return