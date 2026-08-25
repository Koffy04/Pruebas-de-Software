import access_user
import access_item
import access_solicitudes
def main():

    # INTERFAZ DE INICIO
    encargado = False
    solicitud=False
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
                if(solicitud==False):
                    print("----------------------")
                    print(" Lista de los equipos ")
                    print("----------------------\n")
                    access_item.mostrar_equipos()
                    print("----------------------\n")
                    print("¿Que equipo desea solicitar? ")
                    print("----------------------\n")
                    numero = input("Ingrese el numero del equipo:")
                    print("----------------------\n")
                    correo = input("Ingrese su correo:")
                    if access_user.confirmar_tabla_equipos(numero) and access_user.estado_usuario(correo):
                        print("Ingrese la Fecha de inicio de prestamo *Se asume una fecha correcta, de le contrario será rechazada\n")
                        fecha_inicial = input("Formato DD/MM/AAAA:")
                        print("Ingrese la Fecha del final del prestamo *Se asume una fecha correcta, de le contrario será rechazada\n")
                        fecha_final = input("Formato DD/MM/AAAA:")
                        print("Solicitud válida, generando Solicitud para su próxima aprobación/rechazo")
                        if access_user.generar_solicitud(numero,correo,fecha_inicial,fecha_final):
                            print("\n<¡¡Solicitud Generada exitosamente!!>\n")
                            solicitud=True
                            continue
                        else:
                            print("Algo fallo con la solicitud, intentelo denuevo.")
                            continue
                else:
                    print("Usted ya posee una solicitud en espera, Consulte el estado de su solicitud o cancelela")
                    continue
            elif eleccion=="2":
                print("----------------------")
                print(" Ingrese su correo para ver su solicitud")
                print("----------------------\n")
                correo=input("")
                access_solicitudes.estado_solicitud(correo)
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