import datetime as dt
import time

data1 = dt.datetime.now()
time.sleep(60)
data2 = dt.datetime.now()
delta = data2 - data1
def calcular(data_entrada, data_saida, valor_a_pagar):
    data_delta = data_saida - data_entrada
    calcular_minutos = int(data_delta.seconds)/60
    return calcular_minutos * valor_a_pagar

print(calcular(data1, data2, 15))