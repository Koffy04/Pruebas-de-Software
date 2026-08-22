import bd_access

# Inicio
print("Bienvenido")

while True:
    print("Para iniciar sesión, presione 1")
    print("Para registrarse, presione 2")
    eleccion = input()

    if eleccion == "1":
        bd_access.login()
        break
    elif eleccion == "2":
        bd_access.register()
        break
