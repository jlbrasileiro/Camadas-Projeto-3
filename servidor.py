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
import struct
from  preparar import dividir
serialName = "COM5"                  # Windows(variacao de)  detectar sua porta e substituir aqui


def main():
    try:
        # imageR = "./imgs/image.png"
        print("Iniciou o main")
        print(np.asanyarray(imagem1))
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        com1.enable()
        # bit de sacrifico
        rx,nrx = com1.getData(1)
        print("recebeu")
        com1.rx.clearBuffer()
        time.sleep(.1)
        # to vivo?
        rx,nrx = com1.getData(1)
        print("recebeu tamanho")
        time.sleep(.1)
        tamanho = int.from_bytes(rx)
        rx, nrx = com1.getData(tamanho)
        print(rx)
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        txBuffer=int.to_bytes(3)
        com1.sendData(txBuffer)
        time.sleep(.1)
        arquivo1="whatsapp"
        arquivo2="youtube"
        arquivo3="youtubeUm"
        arquivo1Bytes=arquivo1.encode('utf-8')
        tamanho1=int.to_bytes(len(arquivo1Bytes)) 
        arquivo2Bytes=arquivo2.encode('utf-8')
        tamanho2=int.to_bytes(len(arquivo2Bytes))        
        arquivo3Bytes=arquivo3.encode('utf-8')
        tamanho3=int.to_bytes(len(arquivo3Bytes))
        com1.sendData(tamanho1)
        time.sleep(.1)
        com1.sendData(arquivo1Bytes)
        time.sleep(.1)
        com1.sendData(tamanho2)
        time.sleep(.1)
        com1.sendData(arquivo2Bytes)
        time.sleep(.1)
        com1.sendData(tamanho3)
        time.sleep(.1)
        com1.sendData(arquivo3Bytes)
        time.sleep(.1)
        time.sleep(.1)
        
        # rebendo qual
        rx,nrx = com1.getData(1)
        time.sleep(.1)
        print("-------------------------")
        
        print("recebeu  arquivo")
        tamanho = int.from_bytes(rx)
        i=0
        lista=[]
        while i<tamanho:
            tamanhoArquivo,nrx = com1.getData(1)
            time.sleep(.1)
            tamanhoArquivo = int.from_bytes(tamanhoArquivo)
            arquivo,n=com1.getData(tamanhoArquivo)
            time.sleep(.1)
            lista.append(arquivo)
            i+=1
        listaString=[]
        for i in lista:
            palavra=i.decode(encoding="utf-8")
            print("-------------------------")
            print(palavra)
            listaString.append(palavra)
        mandando=f"Arquivos selecionados: {listaString}\n mandando..."
        mandando=mandando.encode('utf-8')
        tamanhomandar=int.to_bytes(len(mandando))
        com1.sendData(tamanhomandar)
        time.sleep(.1)
        com1.sendData(mandando)
        time.sleep(.1)
        podemandar,n = com1.getData(1)
        podemandar=int.from_bytes(podemandar)
        if podemandar==1:
            print("vaicontinuae")
            dicio = {}
            for nome  in listaString:
                if  nome=="whatsapp":
                    codigo = "imgs\imgs\whatsapp.png"
                elif nome=="youtube":
                    
                elif nome=="youtubeUm":
        #as array apenas como boa pratica para casos de ter uma outra forma de dados
            tempo0 = time.time()
            timeout=False
            print("-------------------------")
            print("Comunicação encerrada")
            print("-------------------------")
            com1.disable()
        else:
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
