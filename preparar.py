def dividir(arquivo):
    arquivo1=open(arquivo,"rb").read()
    return [arquivo1[i:i+100] for i in range(0, len(arquivo1),100)]
