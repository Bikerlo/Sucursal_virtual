from my_package import utils
import pandas as pd

path='my_package/datos.xlsx'
xls = pd.ExcelFile(path)
BD = xls.parse('machine')
# Convertir el DataFrame transpuesto a un diccionario
diccionario_resultante = BD.to_dict(orient='records')
billetes=diccionario_resultante[0]

print(billetes)
def update_machine(data):
    for columna, valor in data.items():
        BD.at[0, columna] = valor
    utils.write_to_excel(BD,'machine')
    
def entregar_dinero(monto_a_retirar):
    # Verificar si hay suficiente saldo en el cajero
    global billetes
    saldo_total = sum(denominacion * cantidad for denominacion, cantidad in billetes.items())
    if monto_a_retirar > saldo_total:
        return "Saldo insuficiente en el cajero."
    # Calcular la cantidad de billetes por denominación a entregar
    billetes_entregados = {}
    for denominacion, cantidad_disponible in sorted(billetes.items(), reverse=True):
        cantidad_a_entregar = min(monto_a_retirar // denominacion, cantidad_disponible)
        if cantidad_a_entregar > 0:
            billetes_entregados[denominacion] = cantidad_a_entregar
            monto_a_retirar -= denominacion * cantidad_a_entregar
            billetes[denominacion] -= cantidad_a_entregar

    # Imprimir los billetes entregados
    print("\nBilletes entregados:")
    for denominacion, cantidad in billetes_entregados.items():
        print(f"{cantidad} billetes de {denominacion} COP")
    return "Retiro exitoso. ¡Gracias por usar nuestro cajero!"

def cantidad_dinero():
    global diccionario_resultante
    for k,v in diccionario_resultante[0].items():
        print(f'Billetes de {k}: {v}')