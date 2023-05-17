import socket
from Crypto.Cipher import AES

def Main():
    host = "localhost"
    port = 5000
    address = (host, port)

    # Generamos la llave(16 bytes), una sal y el tipo de encriptación
    llave = b'Esta_es_mi_llave'
    sal = b'Esta_es_mi_-sal-'
    cifrado = AES.new(llave, AES.MODE_EAX, sal)

    # Conexión del socket, utilizando TCP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(address)

    # Abrimos la imagen para lectura
    with open('imagen_original.jpg', 'rb') as archivo:
        datos = archivo.read()

    # Encriptamos los datos
    encriptado = cifrado.encrypt(datos)

    # Enviamos los datos de la imagen
    cliente.sendall(encriptado)
    cliente.send(b'<FIN>')

    print('\n-----------------------')
    print('  Archivo enviado  ')
    print('-----------------------')

    cliente.close()

if __name__ == "__main__":
    Main()
