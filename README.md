# Pruebas-de-Software
Tareas Pruebas de Software y asociados




- *Vacío*: Estado del usuario, Apto para pedir permiso/No autorizado para pedir prestamos. 
- *Vacío*: Registro de quien le entregó el equipo.
- *Vacío*: Pueden haber mas de 1 encargado.
- *Vacío*: Estados del equipo, Mantenimiento/Buen estado/Prestado
- *Riesgo*:El traslado de datos de la planilla a una BD podría generar perdidas de datos, por lo que podría existir la posibilidad de volver a ingresar inventario.
- *Ambiguedad*: Quiere una solución simple, pero que sea confiable al mismo tiempo, lo cual es complejo debido al manejo de situaciones que hay que preveer.
- *Riesgo*: Perdidas de Equipo.
- *Riesgo*: 2 personas podrían solicitar el mismo equipo al mismo tiempo, sin verificar quien lo hizo en la realidad
- *Vacío*: ¿Que se hace en caso de perdida de equipo?


### ¿Preguntas que realizaría al cliente?

¿Cuántas personas estaran como encargadas, hay otra distinción de rol?
¿Está dispuesto a los gastos dedicados al software?
¿Podria explicarme que es lo que debe cumplir para que sea simple el software, y explicarme lo que es confiable?
¿Que tan masivo es el uso y peticiones que recibe actualmente?
Detalleme las condiciones del préstamo, y que cosas actualmente pide al usuario para pedir un prestamo.
¿Hay penalizaciones en caso de perdida o daños a un equipo que afecte al estado del usuario?


### Requerimiento mejorado

El sistema de préstamos de Equipos debe permitir utilizar al que va a pedir un equipo, un usuario, que contenga, su nombre, contraseña, y correo universitario/perteneciente a la organización, para pedir un equipo debe primero pedirlo con 3 días de anticipación y el equipo debe figurar como en Buen estado para ser prestado, adicionalmente debe ser su solicitud aprobada durante ese plazo, para finalmente retirarlo en el periodo del último día.
El usuario tiene una semana hábil (5 días de uso), puede devolver el equipo antes de la fecha límite para devolver el préstamo.
Los encargados tienen la facultad de cambiar los estados de los equipos, además de habilitar o deshabilitar el prestamo a los usuarios.
Si el usuario pierde un equipo se le debe cobrar una multa de reparo + cantidad de días de atraso, lo mismo para un daño del equipo y se le sancionará por 1 mes la facultad de solicitar préstamos.



### Reglas del negocio

*Exclusiones:* El programa no se encargara de gestionar los pagos, ni tampoco los implementará, queda propuesta la lógica de penalización y un calculo del monto, pero cada usuario deberá formalmente arreglar con el encargado la forma de pago, básicamente, el programa no ofrecerá la facultad de pagar por internet.

*Reglas de negocio:* El usuario debe tener un correo perteneciente a la organización para registrarse como campo obligatorio.
Si el usuario se atrasa, tiene un monto fijo de penalización asociado a la cantidad de días de atraso respecto al ultimo día que debería haberlo entregado.
El usuario no puede pedir mas de 1 equipo.
El usuario debe pedir con antelación un equipo y su solicitud debe ser aprobada.

*Alcance:* El usuario será capaz de ver la lista de equipos y el estado del equipo, generar la solicitud de préstamo y ver el estado de esta, si es rechazada o aprobada. Ellos pueden ver si tienen deuda, multa y si son aptos para solicitar prestamo.

El Encargado será capaz de ver las solicitudes por los equipos y usuarios, además de aceptar o rechazar solicitudes, adicionalmente puede ver y modificar la situación de los usuarios.
