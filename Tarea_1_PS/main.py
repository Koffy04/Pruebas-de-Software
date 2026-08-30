import access_user
import access_item
import access_solicitudes

TARIFA_MORA_DIARIA = 2000 

def main():

    # INTERFAZ DE INICIO
    encargado = False

    print("==============================================================")
    print("                          BIENVENIDO                          ")
    print("==============================================================")

    while True:
        print("\n-------------------- OPCIONES DE INICIO --------------------")
        print("| 1. Iniciar sesión                                          |")
        print("| 2. Registrarse                                             |")
        print("| 3. Salir                                                   |")
        print("--------------------------------------------------------------")
        eleccion = input("Su respuesta: ")

        if eleccion == "1":

            print("==============================")
            print("------ INICIO DE SESIÓN ------")
            print("==============================\n")
            encargado = access_user.login()
            break

        elif eleccion == "2":

            print("=========================")
            print("------ REGISTRARSE ------")
            print("=========================\n")
            access_user.register()

        elif eleccion == "3":

            print("\nSaliendo....")
            return

        else:
            print("\n<Valor ingresado inválido. Ingrese de nuevo>\n")

    # INTERFAZ DE SOLICITANTE
    if not encargado:
        while True:

            print("\n")
            print("==================================================================")
            print("                      Interfaz de Solicitante                     ")
            print("==================================================================\n")
            print("-------------------- OPCIONES DE SOLICITANTE ---------------------")
            print("| 1. Ver y solicitar equipo                                      |")
            print("| 2. Ver estado de mi solicitud                                  |")
            print("| 3. Cancelar solicitud *Solo si tiene una solicitud pendiente   |")
            print("| 4. Conoce tu deuda *Solo si tiene una solicitud con deuda      |")
            print("| 5. Salir                                                       |")
            print("------------------------------------------------------------------")
            eleccion = input("Su respuesta: ")

            if eleccion == "1":
                if not access_solicitudes.have_solicitud_correo():
                    if access_user.ver_estado_usuario(encargado):

                        print("------------------------")
                        print(" Ver y solicitar equipo ")
                        print("------------------------\n")

                        access_item.mostrar_equipos(encargado)
                        access_solicitudes.solicitar_equipo()

            elif eleccion=="2":

                print("----------------------------")
                print(" Ver estado de mi solicitud ")
                print("----------------------------\n")
                access_solicitudes.estado_solicitud()

            elif eleccion=="3":

                print("--------------------")
                print(" Cancelar solicitud ")
                print("--------------------\n")
                access_solicitudes.cancelar_solicitud()

            elif eleccion == "4":
                print("-----------------")
                print(" Conoce tu deuda ")
                print("-----------------\n")
                correo=input("")
                access_solicitudes.cancelar_solicitud(correo)

            elif eleccion == "5":
                print("Saliendo...")
                return

            else:
                print("\n<Valor ingresado inválido. Ingrese de nuevo>\n")

    # INTERFAZ DE ENCARGADO
    elif encargado:
        while True:
            print("\n")
            print("==========================================")
            print("           Intefaz de Encargado           ")
            print("==========================================\n")
            print("--------- OPCIONES DEL ENCARGADO ---------")
            print("| 1. Ver solicitudes pendientes          |")
            print("| 2. Ver todos los equipos               |")
            print("| 3. Editar el estado de una máquina     |")
            print("| 4. Ver solicitudes                     |")
            print("| 5. Cambiar el estado de un usuario     |")
            print("| 6. Salir                               |")
            print("------------------------------------------\n")
            eleccion = input("Su respuesta: ")

            if eleccion == "1":

                print("\n----------------------------")
                print(" Ver solicitudes pendientes ")
                print("----------------------------\n")
                access_solicitudes.mostrar_solicitudes(encargado)

            elif eleccion == "2":

                print("\n-----------------------")
                print(" Ver todos los equipos ")
                print("-----------------------\n")

                access_item.mostrar_equipos(encargado)
                input("\nPresione Enter para continuar...")


            elif eleccion == "3":
            
                print("------------------------------")
                print(" Editar estado de una máquina ")
                print("------------------------------\n")
                
                access_item.mostrar_equipos(encargado)
                access_item.ver_estado_equipo()
            
            elif eleccion == "4":

                print("----------------------")
                print(" Cambiar una solicitud ")
                print("----------------------\n")
                print(" Ingrese correo para identificar la solicitud a cambiar")
                print("-----------------------------------------\n")
                correo=input("")
                access_solicitudes.resolver_solicitud(correo)

            elif eleccion == "5":

                access_user.mostrar_usuarios()
                access_user.ver_estado_usuario(encargado)
            
            elif eleccion == "6":
                
                print("Saliendo...")
                return

            else:
                print("\n<Valor ingresado inválido. Ingrese de nuevo>\n")

main()