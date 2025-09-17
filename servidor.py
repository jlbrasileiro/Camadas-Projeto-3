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
from  preparar import dividir, cria_pacote, extrai_pacote
serialName = "COM5"                  # Windows(variacao de)  detectar sua porta e substituir aqui


def main():
    try:
        # imageR = "./imgs/image.png"
        print("Iniciou o main")
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
        txBuffer=int.to_bytes(9)
        com1.sendData(txBuffer)
        time.sleep(.1)
        arquivo1="whatsapp"
        arquivo2="YouTubeMusic"
        arquivo3="oiii"
        arquivo4="camarao"
        arquivo5="estrela"
        arquivo6="nintendo"
        arquivo7="Palmeiras"
        arquivo8="xbox"
        arquivo9="pokebola"
        arquivo1Bytes=arquivo1.encode('utf-8')
        tamanho1=int.to_bytes(len(arquivo1Bytes)) 
        arquivo2Bytes=arquivo2.encode('utf-8')
        tamanho2=int.to_bytes(len(arquivo2Bytes))        
        arquivo3Bytes=arquivo3.encode('utf-8')
        tamanho3=int.to_bytes(len(arquivo3Bytes))
        arquivo4Bytes=arquivo4.encode('utf-8')
        tamanho4=int.to_bytes(len(arquivo4Bytes))
        arquivo5Bytes=arquivo5.encode('utf-8')
        tamanho5=int.to_bytes(len(arquivo5Bytes))
        arquivo6Bytes=arquivo6.encode('utf-8')
        tamanho6=int.to_bytes(len(arquivo6Bytes))
        arquivo7Bytes=arquivo7.encode('utf-8')
        tamanho7=int.to_bytes(len(arquivo7Bytes))
        arquivo8Bytes=arquivo8.encode('utf-8')
        tamanho8=int.to_bytes(len(arquivo8Bytes))
        arquivo9Bytes=arquivo9.encode('utf-8')
        tamanho9=int.to_bytes(len(arquivo9Bytes))
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
        com1.sendData(tamanho4)
        time.sleep(.1)
        com1.sendData(arquivo4Bytes)
        time.sleep(.1)
        com1.sendData(tamanho5)
        time.sleep(.1)
        com1.sendData(arquivo5Bytes)
        time.sleep(.1)
        com1.sendData(tamanho6)
        time.sleep(.1)
        com1.sendData(arquivo6Bytes)
        time.sleep(.1) 
        com1.sendData(tamanho7)
        time.sleep(.1)
        com1.sendData(arquivo7Bytes)
        time.sleep(.1)
        com1.sendData(tamanho8)
        time.sleep(.1)
        com1.sendData(arquivo8Bytes)
        time.sleep(.1)
        com1.sendData(tamanho9)
        time.sleep(.1)
        com1.sendData(arquivo9Bytes)
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
            print(f"palavra {palavra}")
            listaString.append(palavra)
        mandando=f"Arquivos selecionados: {listaString}\n mandando..."
        print(mandando)
        mandando=mandando.encode('utf-8')
        tamanhomandar=int.to_bytes(len(mandando))
        com1.sendData(tamanhomandar)
        time.sleep(.1)
        com1.sendData(mandando)
        time.sleep(.1)
        podemandar,n = com1.getData(1)
        podemandar=int.from_bytes(podemandar)
        if podemandar==1:
            print("-------------------------\n")
            print("vaicontinuae")
            dicio = {}
            # print(dividir("imgs\\whatsapp.png"))
            for nome  in listaString:
                print(f"nome{nome}")
                if  nome=="whatsapp":
                    codigo = dividir("imgs\\whatsapp.png")
                    dicio['0']=codigo
                elif nome=="YouTubeMusic":
                    codigo = dividir("imgs\\YouTubeMusic.png")
                    dicio['1']=codigo
                elif nome=="oiii":
                    codigo = dividir("imgs\\oiii.png")
                    dicio['2']=codigo
                elif nome=="camarao":
                    codigo = dividir("imgs\\camarao.png")
                    dicio['3']=codigo
                elif nome=="estrela":
                    codigo = dividir("imgs\\estrela.png")
                    dicio['4']=codigo
                elif nome=="nintendo":
                    codigo = dividir("imgs\\nintendo.png")
                    dicio['5']=codigo
                elif nome=="Palmeiras":
                    codigo = dividir("imgs\\Palmeiras.png")
                    dicio['6']=codigo
                elif nome=="xbox":
                    codigo = dividir("imgs\\xbox.png")
                    dicio['7']=codigo
                elif nome=="pokebola":
                    codigo = dividir("imgs\\pokebola.png")
                    dicio['8']=codigo
            # print(dicio.keys())
            max=0
            for n,t in dicio.items():
                print(f"arquivo{n}, cont{len(t)}")
                if len(t)>max:
                    max=len(t)
            i=0
            print(f"max{max}")
            # exemplo = dicio["2"]
            # pacote=cria_pacote(0,len(dicio["2"]),1,exemplo[0])
            # print(pacote)
            # com1.sendData(pacote)
            # time.sleep(.1)    
            while True:
                # print("foi primeiro loop")
                if i>max:
                    break
                a=0
                for arquivo,n in dicio.items():
                    # print("-------------------------\n")
                    # print(f"nome {arquivo}, tamanho {len(n)}")
                    if i>=len(n):
                        pass
                    else:
                        print("-------------------------\n")
                        print(f"index {i}, tamanho {len(n)}")   
                        pacote=cria_pacote(a,len(n),i+1,n[i])
                        com1.sendData(pacote)
                        time.sleep(.1)
                        tempoInicial = time.time()
                        tempoFinal = time.time()
                        index=3
                        print(index)
                        com1.rx.clearBuffer()    
                        index, payload, total, numero, correto = extrai_pacote(com1=com1)
                        # if (index )
                        if (index == 0) or (numero != (i+1)) or (a!=total):
                            i =numero-1
                            a=total
                            while True:
                                pacote=cria_pacote(a,len(n),i+1,n[i])
                                com1.sendData(pacote)
                                time.sleep(.1)
                                index, payload, total, numero, correto = extrai_pacote(com1=com1)            
                                if index == 1:
                                    break
                        if index == 2:
                            i=i-1
                            print(f"index {i}, tamanho {len(n)}----------")   
                            print("pausou")
                            pass
                        if index ==1:
                            print(f"index {index}, t0 {tempoInicial} tf {tempoFinal}, arquivo{total}, meu arquivo{a}")
                            a+=1
                            pass
                        
                i+=1
                # break
            print("terminou os loops")
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
