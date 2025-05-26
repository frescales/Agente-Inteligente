from datetime import date

def hoy():
    return date.today()

def primer_dia_mes():
    h = hoy()
    return date(h.year, h.month, 1)
