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
from preparar import extrai_pacote,cria_pacote
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
        #Envia biyte de sacrificio
        sacrificio=b'00'
        com1.sendData(sacrificio)
        print("-------------------------")
        print("Byte de sacrificio enviado")
        print("-------------------------")
        time.sleep(0.1)
        m2server = "Ola mundo"
        m2server = m2server.encode(encoding="utf-8")
        print(m2server)
        
        lenth=int.to_bytes(len(m2server))
        
        com1.sendData(lenth)
        time.sleep(0.1)
        com1.sendData(m2server)


        #Recebe tmanho da lista de arquivos
        rxBuffer, nRx = com1.getData(1)
        qte=int.from_bytes(rxBuffer)
        print("--------------------------------------------------------------------------------------------------")
        print(f"Existem {qte} arqivos disponiveis")
        print("--------------------------------------------------------------------------------------------------")
        
        i=1
        arquivos=[]
        while i <= qte:
            rxBuffer, nRx = com1.getData(1)
            neme_len=int.from_bytes(rxBuffer)
            rxBuffer, nRx = com1.getData(neme_len)
            file_neme=rxBuffer.decode(encoding="utf-8")
            arquivos.append(file_neme)
            print(f"{i}. {file_neme}")
            i+=1
        
        print("--------------------------------------------------------------------------------------------------")
        arquivos_desejeados=[]
        while True:
            file_number=int(input("Quel o numero do arquivo desejado? (Digite 0 para finalizar)"))
            if file_number==0:
                break 
            arquivos_desejeados.append(arquivos[file_number-1])
        
        len_d=int.to_bytes(len(arquivos_desejeados))
        com1.sendData(len_d)
        time.sleep(0.1)

        print("-------------------------")
        print("Solicitando arquivos")
        print("-------------------------")
        for arquivo in arquivos_desejeados:
            print(arquivo)
            arquivo_bytes=arquivo.encode(encoding="utf-8")
            len_a=int.to_bytes(len(arquivo_bytes))
            com1.sendData(len_a)
            time.sleep(.1)
            com1.sendData(arquivo_bytes)
            time.sleep(.1)
        print("------------------------------------------------------------------------------------------")
        rxBuffer, nRx = com1.getData(1)
        lem_m=int.from_bytes(rxBuffer)
        rxBuffer, nRx = com1.getData(lem_m)
        print(rxBuffer.decode(encoding="utf-8"))
        print("-----------------------------------------------------------------------------------------")
        conf=int(input("Confirmar (1), cancelar (0)"))
        com1.sendData(int.to_bytes(conf))
        if conf !=1:
            print("-------------------------")
            print("Comunicação encerrada")
            print("-------------------------")
            com1.disable()

        index,payload,total,numero,correto=extrai_pacote(com1=com1,lista_desejados=arquivos_desejeados)
        # Encerra comunicação
        print(index)
        print(numero)
        print(correto)
        pacote=cria_pacote(index=index,total=total,nPacote=numero)
        com1.sendData(pacote)
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
