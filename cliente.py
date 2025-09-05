#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
from conversores import decimal_para_bytes_ieee754, bytes_ieee754_para_decimal

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)  detectar sua porta e substituir aqui


def main():
    try:
        
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
           
             
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        print(rxBuffer)
        com1.rx.clearBuffer()
        time.sleep(.1)

        print("-------------------------------------------------------")
        print("Pronto para comunicação")

        numeros=[]
        #t_0=time.time()
        qte,nRx=com1.getData(4)
        qte=bytes_ieee754_para_decimal(qte)
        print(f"Quantidade de números:{qte}")
        print("-------------------------------------------------------")
        i=0
        while i<round(qte):
            #t_0=time.time()
            rxBuffer, nRx = com1.getData(4)
            #codigo para conveter IEEE em decimal
            n=bytes_ieee754_para_decimal(rxBuffer)
            print(f"{n:.6f}")
            time.sleep(0.1)
            numeros.append(n)
            i+=1
        print("-------------------------------------------------------")
        print("Pronto para enviar a soma")
        txBuffer=sum(numeros)
        print (f"Soma: {txBuffer:.6f}")
        #codigo para converter decimal para IEEE 
        txBuffer=decimal_para_bytes_ieee754(txBuffer)
        print ("Enviando soma")
        com1.sendData(txBuffer)
        print("Soma enviada")

            
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
