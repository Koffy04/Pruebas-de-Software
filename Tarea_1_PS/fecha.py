from datetime import datetime, date, timedelta

# fecha_actual = date.today().strftime("%d/%m/%Y")
fecha_actual = "05/09/2026"
lista = []

# Get-er fecha_actual
def get_actual():
    return datetime.strptime(fecha_actual,'%d/%m/%Y')

def print_today():
    return fecha_actual

# 3 días hábiles en base a la fecha actual
def plus_bussiness_3days():

    obj = get_actual()
    count = 0

    while count < 3:
        obj += timedelta(days=1)
        if obj.weekday() <= 4:
            count += 1

    fecha = obj.strftime('%d/%m/%Y')

    return fecha

# X días en base a una fecha arbitraria
def plus_7days(date):
    try:
        obj = datetime.strptime(date, '%d/%m/%Y')
    except ValueError:
        print("[Error] Formato inválido. Debe usar exactamente DD/MM/AAAA (ej. 15/04/2026).\n")
        return False

    objx = (obj + timedelta(days=7))
    fecha = objx.strftime('%d/%m/%Y')

    return fecha  

# Compara dos fechas, verificando si la fecha arbitaria cumple con ser 3 días mayor que la original
def compare_date_past(date):

    try:
        obj = datetime.strptime(date, "%d/%m/%Y")
    except ValueError:
        print("[Error] Formato inválido. Debe usar exactamente DD/MM/AAAA (ej. 15/04/2026).\n")
        return False

    obj_act = get_actual()

    obj_3plus = plus_bussiness_3days()
    obj_plus = datetime.strptime(obj_3plus, '%d/%m/%Y')
    
    if obj < obj_act:
        print(f"[Error] La fecha es pasado a la fecha actual {obj_act.strftime('%d/%m/%Y')}")
        return False

    elif obj < obj_plus:
        print(f"[Error] La fecha es menor a la fecha mínima {obj_plus.strftime('%d/%m/%Y')}")
        return False

    return True

# Muestra la semana hábil, los printea y los guarda en una lista global
def show_week(date):
    global lista
    lista.clear()

    date_i = datetime.strptime(date, '%d/%m/%Y')
    date_f = datetime.strptime(plus_7days(date), '%d/%m/%Y')

    print(f"Fechas disponibles (desde {date_i.strftime('%d/%m/%Y')} hasta {date_f.strftime('%d/%m/%Y')} para devolver: ")

    while date_i <= date_f:

        if date_i.weekday() <= 4:
            lista.append(date_i)
            print(f"- {date_i.strftime('%d/%m/%Y')}")

        date_i += timedelta(days=1)

# Compara la fecha con las fechas en la lista
def compare_date_future(date):

    try:
        obj = datetime.strptime(date, '%d/%m/%Y')
    except ValueError:
        print("[Error] Formato inválido. Debe usar exactamente DD/MM/AAAA (ej. 15/04/2026).\n")
        return False

    for dt in lista:
        if obj == dt:
            return True

    print("[Error] Fecha no pertenece al rango mostrado")
    return False

# Verifica si una fecha es mayor a la fecha actual
def commpare_simple(date):

    try:
        obj = datetime.strptime(date, '%d/%m/%Y')
    except ValueError:
        print("[Error] Formato inválido. Debe usar exactamente DD/MM/AAAA (ej. 15/04/2026).\n")
        return False

    objx = get_actual()

    if obj < objx:
        return False

    return True