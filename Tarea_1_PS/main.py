import access_user
import access_item
import access_solicitudes

TARIFA_MORA_DIARIA = 2000 

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
            print("4. Conoce tu deuda *Solo si tiene una solicitud")
            print("5. Salir")
            eleccion = input("Su respuesta: ")

            if eleccion == "1":
                if access_user.have_solicitudes() == False:

                    if access_user.estado_usuario():

                        print("----------------------")
                        print(" Lista de los equipos ")
                        print("----------------------\n")

                        access_item.mostrar_equipos("")
                        
                        print("------------------------------")
                        print(" ¿Que equipo desea solicitar? ")
                        print("------------------------------\n")

                        id = input("Ingrese el ID del equipo: ")
                        if access_item.confirmar_tabla_equipos(id):

                            # HACER FUNCIÓN DE VER FECHA
                            fecha_inicial = access_solicitudes.solicitar_fecha_prestamo()
                            fecha_final = access_solicitudes.solicitar_fecha_fin(fecha_inicial)
                            print("------------------------------\n")
                            print("Solicitud válida, generando Solicitud para su próxima aprobación/rechazo")
                            if access_solicitudes.generar_solicitud(id,fecha_inicial,fecha_final):
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
                print("-----------------------------------------")
                print(" Ingrese su correo para ver su solicitud ")
                print("-----------------------------------------\n")
                correo=input("")
                access_solicitudes.cancelar_solicitud(correo)

            elif eleccion == "4":
                print("-----------------------------------------")
                print(" Ingrese su correo para ver su solicitud ")
                print("-----------------------------------------\n")
                correo=input("")
                access_solicitudes.cancelar_solicitud(correo)

            elif eleccion == "5":
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
            print("4. Cambiar el estado de una solicitud")
            print("5. Cambiar el estado de un usuario")
            print("6. Salir")
            eleccion = input()

            if eleccion == "1":
                print("----------------------")
                print(" Lista de solicitudes")
                print("----------------------\n")
                access_solicitudes.mostrar_solicitudes("all")
                continue
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
                print("----------------------")
                print(" Cambiar una solicitud ")
                print("----------------------\n")
                print(" Ingrese correo para identificar la solicitud a cambiar")
                print("-----------------------------------------\n")
                correo=input("")
                access_solicitudes.resolver_solicitud(correo)
                return
            elif eleccion == "5":
                print("----------------------")
                print(" Cambiar estado de usuario")
                print("----------------------\n")
                print(" Ingrese correo para identificar la usuario a cambiar")
                print("-----------------------------------------\n")
                correo=input("")
                print(" Ingrese nuevo estado de usuario")
                print("-----------------------------------------\n")
                nuevo_estado=input("")
                access_user.cambiar_estado_usuario(correo, nuevo_estado)
                return
            elif eleccion == "6":
                return

            else:
                print("\n<Valor ingresado inválido. Ingrese de nuevo>\n")

main()