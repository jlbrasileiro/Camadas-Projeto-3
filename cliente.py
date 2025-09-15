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
import keyboard


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

        pause=True
        

        index_ant=42
        numero_ant=42
        payloads=[]
        arquivos_completos=0
        start=time.time()
        pacote=cria_pacote(index=1,total=0,nPacote=0,payload=b'00')
        while True:
            if keyboard.is_pressed("a"):
                print ("foi")
                pause=True
                time.sleep(0.1)

            while True:
                buffer_len=com1.rx.getBufferLen()
                now=time.time()
                if (now-start>1) and buffer_len<10:
                    com1.sendData(pacote)
                    start=time.time()
                elif buffer_len>=10:
                    break
        
            index,payload,total,numero,correto=extrai_pacote(com1=com1)
            com1.rx.clearBuffer()
            print(index)
            #print(numero)
            #print(total)
            #print(correto)
            #print (payload)
            
            
            
            if index_ant!=index or numero!=numero_ant:
                adicinar=True

            if numero==1 and correto==True:
                payloads.append(payload)
                adicinar=False

            elif total>=numero and correto==True and adicinar==True:
                payloads[index]=payloads[index]+payload
                adicinar=False
            #envia se foi correto
            if numero==total and correto==True:

                arquivos_completos+=1
                print (f'Progresso {arquivos_desejeados[index]}: Completo!')

            if correto==True and pause==False:
                pacote=cria_pacote(index=1,total=index,nPacote=numero,payload=b'00')
                com1.sendData(pacote)
                start=time.time()
                print (f'Progresso {arquivos_desejeados[index]}: {100*numero/total}%')
                print("------------------------------------------------------------------------------------------------------------")
            elif correto==True and pause==True:
                pacote=cria_pacote(index=2,total=index,nPacote=numero,payload=b'00')
                com1.sendData(pacote)
                while pause==True:
                    if keyboard.is_pressed("a"):
                        pause=False
                        print("relese")
                        pacote=cria_pacote(index=1,total=index,nPacote=numero,payload=b'00')
                        com1.sendData(pacote)
            else:
                pacote=cria_pacote(index=0,total=total,nPacote=numero,payload=b'00')
                com1.sendData(pacote)
            index_ant=index
            numero_ant=numero
            if len(arquivos_desejeados)==arquivos_completos:
                break
        print("------------------------------------------------------------------------------------------------------------")
        print("Todos os arquivos recebidos com sucesso!!")
        print("Iniciando converção e salvamento")
        print("------------------------------------------------------------------------------------------------------------")
        #print(payloads)
        
        i=0
        while i<len(arquivos_desejeados):
            arquivo="./imgs/"+arquivos_desejeados[i]+".png"
            print(arquivo)
            f=open(arquivo, "wb")
            payload=payloads[i]
            f.write(payload)
            f.close()
            i+=1
        
        print("Arquivos salvos")
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
