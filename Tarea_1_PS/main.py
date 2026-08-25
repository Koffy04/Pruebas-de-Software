import access_user
import access_item
import access_solicitudes
import fecha

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
        print("=========================\n")
        print("------ OPCIONES DE Solicitante ------")

        while True:

            print("1. Ver y solicitar equipo")
            print("2. Ver estado de mi solicitud")
            print("3. Cancelar solicitud *Solo si tiene una solicitud pendiente")
            print("4. Salir")
            eleccion = input("Su respuesta: ")

            if eleccion == "1":
                if access_user.have_solicitudes() == False:

                    print("----------------------")
                    print(" Lista de los equipos ")
                    print("----------------------\n")

                    access_item.mostrar_equipos("")
                    
                    print("------------------------------")
                    print(" ¿Que equipo desea solicitar? ")
                    print("------------------------------\n")

                    if access_user.estado_usuario():

                        id = input("Ingrese el ID del equipo:")
                        if access_item.confirmar_tabla_equipos(id):

                            # HACER FUNCIÓN DE VER FECHA
                            print("Ingrese la Fecha de inicio de prestamo *Se asume una fecha correcta, de le contrario será rechazada\n")
                            fecha_inicial = input("Formato DD/MM/AAAA:")
                            print("Ingrese la Fecha del final del prestamo *Se asume una fecha correcta, de le contrario será rechazada\n")
                            fecha_final = input("Formato DD/MM/AAAA:")
                            print("Solicitud válida, generando Solicitud para su próxima aprobación/rechazo")

                            if access_solicitudes.generar_solicitud(id,correo,fecha_inicial,fecha_final):

                                print("\n<¡¡Solicitud Generada exitosamente!!>\n")
                                continue

                            else:

                                print("Algo fallo con la solicitud, intentelo denuevo.")
                                continue
                else:

                    print("Usted ya posee una solicitud en espera, Cumpla con la solicitud o cancelela")
                    continue

            elif eleccion=="2":

                print("-----------------------------------------")
                print(" Ingrese su correo para ver su solicitud ")
                print("-----------------------------------------\n")
                correo=input("")
                access_solicitudes.estado_solicitud(correo)

            elif eleccion=="3":
                print("hola")

            elif eleccion == "4":
                return

            else:
                print("\n<Valor ingresado inválido. Ingrese de nuevo>\n")

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
                access_item.mostrar_equipos("all")
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