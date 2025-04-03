import mysql
import mysql.connector
import pandas as pd

class Database: #Classe vinculada ao banco de dados MySQL
    def input(placa, cpf, data_entrada): #Conecta ao banco de dados car_registro e insere registros na tabela car.
        connect = mysql.connector.connect(
            host="Stopcar_db",
            root="root",
            password="",
            database="car_registro"
        )
        cursor = connect.cursor()
        input = f"INSERT INTO car(plc_veiculo, cpf_dono_veiculo, entrada_veiculo) VALUES '{placa}, {cpf}, {data_entrada};"
        cursor.execute(input)
        connect.commit()
        print("Carro registrado com sucesso!")
        
    def output(data_saida): #Conecta ao banco de dados car_registro e insere registros na tabela car_out.
        connect = mysql.connector.connect(
            host="Stopcar_db",
            root="root",
            password="",
            database="car_registro"
        )
        cursor = connect.cursor()
        output = f"INSERT INTO car_out(saida_veiculo) VALUES '{data_saida}';"
        cursor.execute(output)
        connect.commit()
        print("Saída registrada com sucesso!")
        
    def consulta(banco, veiculo, cpf_dono): #Realiza uma Query dentro do banco de dados.
        connect = mysql.connector.connect(
        host="Stopcar_db",
        root="root",
        password="",
        database="car_registro"
    )
        cursor = connect.cursor()
        consulta = f"SELECT * FROM '{banco}';"
        if veiculo == "" and cpf_dono == "":
            cursor.execute(consulta)
            table = cursor.fetchall()
        else:
            consulta = f"SELECT * FROM '{banco}' WHERE plc_veiculo = '{veiculo}' OR cpf_dono_veiculo = '{cpf_dono}';"
            cursor.execute(consulta)
            table = cursor.fetchall()
        print(pd.DataFrame(table))
class Configures: #Classe para serviços
    def calculo_cpf(cpf): #Realiza o calculo para verificação dos dígitos do CPF.
        digitos = [int(cpf[0]*10),int(cpf[1]*9),int(cpf[2]*8),int(cpf[3]*7),int(cpf[4]*6),int(cpf[5]*5),int(cpf[6]*4),int(cpf[7]*3),int(cpf[8]*2)] #Lista para facilitar a soma dos dados
        confirma_digito10 = 11 - (sum(digitos)%11) #Verificador do dígito: calculando 11 - o resto da divisão.
        aprovar = False
        if (sum(digitos)%11) >= 10: #Verifica se o cálculo anterior retorna um número maior que 10, caso sim, o 10° dígito é 0.
            confirma_digito10 == 0
            lista_calculo_digitos = [] #Lista para facilitar a soma dos dados.
            multiplicador = 11 #Multiplicador
            for calculate in range(cpf[0:10]): #Laço para realizar os cálculos, baseados na quantidade de dados dentro da variável cpf.
                lista_calculo_digitos.append(calculate*multiplicador) #Adiciona a cada repetição, a multiplicação entre o multiplicador e o index.
                multiplicador -= 1
            confirma_digito11 = 11 - (sum(lista_calculo_digitos)%11) 
            if sum(lista_calculo_digitos)%11 >= 10: #Verifica se o cálculo anterior retorna um número maior ou igual à 10, caso sim, o 11° dígito é 0.
                confirma_digito11 = 0
                if confirma_digito10 == cpf[9] and confirma_digito11 == cpf[10]: #Caso os resultados das variáveis confirma_digito sejam iguais aos 10° e 11° dígitos do cpf, retorne valor booleano para a variável aprovar.
                    aprovar = True
                else:
                    aprovar = False
            else:
                if confirma_digito10 == cpf[9] and confirma_digito11 == cpf[10]:
                    aprovar = True
                else:
                    aprovar = False
            return aprovar
        else:
            lista_calculo_digitos = [] #Lista para facilitar a soma dos dados.
            multiplicador = 11 #Multiplicador
            for calculate in range(cpf[0:10]): #Laço para realizar os cálculos, baseados na quantidade de dados dentro da variável cpf.
                lista_calculo_digitos.append(multiplicador*calculate) #Adiciona a cada repetição, a multiplicação entre o multiplicador e o index.
                multiplicador -= 1
            confirma_digito11 = 11 - (sum(lista_calculo_digitos)%11)
            if sum(lista_calculo_digitos)%11 >= 10: #Verifica se o cálculo anterior retorna um número maior que 10, caso sim, o 11° dígito é 0.
                confirma_digito11 = 0
                if confirma_digito10 == cpf[9] and confirma_digito11 == cpf[10]: #Caso os resultados das variáveis confirma_digito sejam iguais aos 10° e 11° dígitos do cpf, retorne valor booleano para a variável aprovar.
                    aprovar = True
                else:
                    aprovar = False
            else:
                if confirma_digito10 == cpf[9] and confirma_digito11 == cpf[10]:
                    aprovar = True
                else:
                    aprovar = False
            return aprovar
                    
    def calcular_valores(data_entrada, data_saida): #Calcula a diferença de tempos e retornar minutos.
        data_delta = data_saida - data_entrada
        calcular_minutos = int(data_delta.seconds)/60
        cobranca = 12 #O valor base da primeira hora é 12 reais.
        valor_a_pagar = 0
        if calcular_minutos > 15 and calcular_minutos <= 75:
            valor_a_pagar = cobranca
        elif calcular_minutos > 75: #A partir da primeira hora, entre as primeiras 5 horas, é cobrada a taxa de 4 centavos por minuto.
            minutos_extras = 0.40
            valor_a_pagar = cobranca + ((calcular_minutos - 75)*minutos_extras)
            if calcular_minutos > 315:
                minutos_extras = 0.75
                valor_a_pagar = valor_a_pagar + ((calcular_minutos - 315)*minutos_extras)
        return valor_a_pagar
        
            