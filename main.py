import datetime as dt
from flask import Flask, render_template, flash, request, redirect, url_for
import mysql

#BEM VINDO!#
#Estacionamento SOPTCAR#

#Funções:

def conection_db_in(placa, cpf, entrada):#Conecta ao banco de dados car_registro e insere registros na tabela car.
    connect = mysql.connector.connect(
        host="Stopcar_db",
        root="root",
        password="",
        database="car_registro"
        )
    cursor = connect.cursor()
    input = f"INSERT INTO 'car'(plc_veiculo, cpf_dono_veiculo, entrada_veiculo) VALUES ('{placa}', '{cpf}', '{entrada}');"
    cursor.execute(input)
    connect.commit()
    confirm = print("ENTRADA REALIZADA COM SUCESSO!")    
    return confirm

def connection_db_out(data_saida): #Conecta ao banco de dados car_registro e insere registros na tabela car_out.
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
    confirm = print("ENTRADA REALIZADA COM SUCESSO!")
    return confirm
    
def connection_db_select(banco, veiculo, cpf_dono): #Realiza uma Query dentro do banco de dados.
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
    return print(table)

def calculo_cpf(cpf): #Realiza cálculos para verificador dos últimos 2 dígitos do CPF
    digitos = [int(cpf[0]*10),int(cpf[1]*9),int(cpf[2]*8),int(cpf[3]*7),int(cpf[4]*6),int(cpf[5]*5),int(cpf[6]*4),int(cpf[7]*3),int(cpf[8]*2)] #Lista para facilitar a soma dos dados
    confirma_digito10 = 11 - (sum(digitos)%11) #Verificador do dígito: calculando 11 - o resto da divisão.
    if (sum(digitos)%11) >= 10: #Verifica se o cálculo anterior retorna um número maior que 10, caso sim, o 10° dígito é 0.
        confirma_digito10 == 0
        lista_calculo_digitos = [] #Lista para facilitar a soma dos dados.
        multiplicador = 11 #Multiplicador
        for calculate in range(cpf[0:10]): #Laço para realizar os cálculos, baseados na quantidade de dados dentro da variável cpf.
            lista_calculo_digitos.append(calculate*multiplicador) #Adiciona a cada repetição, a multiplicação entre o multiplicador e o index.
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
    return calcular_minutos

#Script:
while (True):
    opcao = int(input("Selecione a opção desejada"+"\n1-[Registrar Veículo]"+"\n2-[Expedir Veículo]"+"\n3-[Verificar Preços]\n")) #Painel inicial com opções: 1- entrada, 2- saída e 3- verificação de preços.
    listaTempo = [] #Predefinição da lista.
    if opcao == 1:
        #1- Registrar dados do veículo (input)
        lista_placa = [] #Lista para receber valores string
        for contador in range(3): #Laço para disponibilizar até 3 tentativas para o usuário cadastrar a placa.
            if len(lista_placa) < 7:
                placa = input("Digite a placa do veículo\nformat: XXX-1X25\n") #Variável para receber os valores das placas
                linha = 0 
                for contador2 in placa:
                    linha += 1
                    if (linha == 1 and contador2.isdigit()) or (linha == 2 and contador2.isdigit()) or (linha == 3 and contador2.isdigit()) or (linha == 5 and contador2.isdigit()) or (linha == 4 and not contador2.isdigit()) or (linha == 6 and not contador2.isdigit()) or (linha == 7 and not contador2.isdigit()):
                        #Tratamento para os caracteres para garantir que o formato esteja correto ex: XXX1X11
                        lista_placa.clear
                        print("FORMATO INVÁLIDO!!")
                    else:
                        lista_placa.append(contador2)
            else:
                break
        placa = str(lista_placa[0]+lista_placa[1]+lista_placa[2]+lista_placa[3]+lista_placa[4]+lista_placa[5]+lista_placa[6]) #Concatenar todos os endereços dentro da lista na variável placa, string .
        
        for contador2 in range(3): #Laço para disponibilizar até 3 tentativas para o usuário cadastrar o cpf.
            cpf = input(f"Digite o CPF do dono do veículo {placa}: ")

            if len(cpf) != 11 and not cpf.isdigit():
                print("CPF INVÁLIDO, TENTE NOVAMENTE!")
            elif contador2 == 3:
                print("CPF INVÁLIDO, FIM DAS TENTATIVAS.")
                break
            
            
            
        data_entrada = dt.datetime.now()
    # elif opcao == 2: #2- Registrar Saída do veículo (output) com preços.
        