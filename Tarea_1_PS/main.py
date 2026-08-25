import access_user
import access_item

def main():

    # INTERFAZ DE INICIO
    encargado = False
    print("Bienvenido a la aplicación de reserva de equipos")

    while True:
        print("\n------ OPCIONES DE INICIO ------")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        eleccion = input("Su respuesta: ")

        if eleccion == "1":
            print("\n------ INICIO DE SESIÓN ------")
            encargado = access_user.login()
            break

        elif eleccion == "2":
            print("\n------ REGISTRARSE ------")
            access_user.register()

        elif eleccion == "3":
            print("\nSaliendo....")
            return

    # INTERFAZ DE SOLICITANTE
    if not encargado:
        print("\n")
        print("=========================")
        print(" Interfaz de Solicitante ")
        print("=========================")
        print("------ OPCIONES DE Solicitante ------")
        while True:
            print("1. Ver equipos y solicitar equipo")
            print("2. Ver estado de mi solicitud")
            print("3. Cancelar solicitud *Solo si tiene una solicitud pendiente")
            if eleccion == "1":
                print("----------------------")
                print(" Lista de los equipos ")
                print("----------------------\n")
                access_item.mostrar_equipos()
                input("\nPresione Enter para continuar...")
                continue
            elif eleccion=="2":
                print("hola")
            elif eleccion=="3":
                print("hola")
            else:
                print("hola")
    # INTERFAZ DE ENCARGADO
    else:
        while True:
            print("\n")
            print("======================")
            print(" Intefaz de Encargado ")
            print("======================\n")
            print("------ OPCIONES DE ENCARGADO ------")
            print("1. Ver solicitudes pendientes")
            print("2. Ver todas las máquinas")
            print("3. Editar el estado de una máquina")
            print("4. Salir")
            eleccion = input()

            if eleccion == "1":
                # INTERFAZ SOLICITUDES PENDIENTES
                return
            elif eleccion == "2":

                print("----------------------")
                print(" Lista de los equipos ")
                print("----------------------\n")
                access_item.mostrar_equipos()
                input("\nPresione Enter para continuar...")
                continue

            elif eleccion == "3":
            
                print("----------------------")
                print(" Lista de los equipos ")
                print("----------------------\n")
                
                access_item.mostrar_estados()
                access_item.mostrar_estado_individual()

                n_sure = input("\n¿Está seguro que quiere modificar este equipo? Y/N")
                if n_sure.upper() == "Y":
                    access_item.mostrar_estado_individual()
                elif n_sure.upper() == "N":
                    continue
                else:
                    print("\n<Valor ingresado inválido. Volviendo al inicio del Encargado>\n")
                    continue

                return
            elif eleccion == "4":
                
                return

            else:
                print("\n<Valor ingresado inválido. Ingrese de nuevo>\n")

main()