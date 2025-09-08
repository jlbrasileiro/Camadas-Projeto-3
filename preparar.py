from enlace import *

def dividir(arquivo):
    arquivo1=open(arquivo,"rb").read()
    return [arquivo1[i:i+100] for i in range(0, len(arquivo1),100)]


def cria_pacote(index:int,total:int,nPacote:int,payload):
    if nPacote>total:
        pass

    index = index.to_bytes()
    pkg_len = payload.len()
    pkg_len = pkg_len.to_bytes()
    total = total.to_bytes()
    nPacote = nPacote.to_bytes()

    free = b"00"
    conf = 42
    conf = conf.to_bytes()

    pacote = index+pkg_len+total+nPacote+free*3+payload+conf*3
    
    return pacote

def extrai_pacote(com1:enlace,lista_desejados):
    #Extrai o head
     index_arq,n = com1.getData(1)
     pkg_len,n = com1.getData(1)
     t_pkg,n = com1.getData(2)
     n_pkg,n = com1.getData(2)
     free = com1.getData(4)

     #Converte os valores para int 
     index_arq = int.from_bytes(index_arq)
     pkg_len = int.from_bytes(pkg_len)
     t_pkg = int.from_bytes(t_pkg)
     n_pkg = int.from_bytes(n_pkg)

     #Extrai o pyload
     payload,n = com1.getData(pkg_len)

     #Extrai EOF
     i = 0
     correto = True
     while i<3:
         conf,n = com1.getData(1)
         conf = int.from_bytes(conf)
         if conf != 42 or n_pkg>t_pkg:
             correto = False
         i+=1
    
     nome_arq = lista_desejados[index_arq]
     nome_arq = nome_arq+".png"
     return nome_arq, payload, n_pkg, correto