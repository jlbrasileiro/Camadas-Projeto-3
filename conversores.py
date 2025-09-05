import struct

def decimal_para_bytes_ieee754(numero):
    bytes_ieee = struct.pack('!f', numero)
    return bytes_ieee



def bytes_ieee754_para_decimal(bytes_ieee):
    if len(bytes_ieee) != 4:
        raise ValueError("O array deve conter exatamente 4 bytes.")
    
    numero_decimal = struct.unpack('!f', bytes_ieee)[0]
    return numero_decimal

