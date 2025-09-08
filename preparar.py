def dividir(arquivo):
    arquivo1=open(arquivo,"rb").read()
    return [arquivo1[i:i+100] for i in range(0, len(arquivo1),100)]


def cria_pacote(index:int,total:int,nPacote:int,payload):
    if nPacote>total:
        pass
    index = index.to_bytes()
    pkg_len = len(payload)
    pkg_len = pkg_len.to_bytes()
    total = total.to_bytes(4)
    nPacote = nPacote.to_bytes()

    free = b"00"
    conf = 42
    conf = conf.to_bytes()

    pacote = index+pkg_len+total+nPacote+free*3+payload+conf*3
    
    return pacote