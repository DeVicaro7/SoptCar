import datetime as dt
import classes as cl
import pandas as pd

#BEM VINDO!#
#Estacionamento SOPTCAR#
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
            if cl.Configures.calculo_cpf(cpf) == False: #Caso o método calculo_cpf retornar Falso, o usuário terá mais 3 tentativas.
                if contador2 < 3:
                    cpf = ""
                    print(f"CPF INVÁLIDO!!\nTentativas restantes: {contador2}")
                else:
                    cpf = ""
                    print("Excesso de tentativas, por favor tente novamente mais tarde!")
            else:
                break
            
        data_entrada = dt.datetime.now() #Registrando em variável, a data de entrada.
        cl.Database.input(placa, cpf, data_entrada) #Criando um registro no banco de dados.
    elif opcao == 2: #SAVEPOINT: elif opcao == 2: #2- Registrar Saída do veículo (output) com preços.
        data_saida = dt.datetime.now()
        cl.Database.output(data_saida)
