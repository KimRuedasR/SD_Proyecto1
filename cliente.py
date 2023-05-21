import socket
from Crypto.Cipher import AES

def Main():
    host = "localhost"
    port = 5000
    address = (host, port)

    # Generamos la llave (16 bytes), una sal y el tipo de encriptación
    llave = b'Esta_es_mi_llave'
    sal = b'Esta_es_mi_-sal-'

    # Conexión del socket, utilizando TCP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(address)

    # Abrimos la imagen para lectura en modo binario
    with open('imagen_original.jpg', 'rb') as archivo:
        datos = archivo.read()

    # Inicializamos el objeto de cifrado AES
    cifrado = AES.new(llave, AES.MODE_EAX, sal)

    # Encriptamos los datos
    encriptado = cifrado.encrypt(datos)

    # Enviamos los datos de la imagen
    cliente.sendall(encriptado)
    cliente.send(b'<FIN>')

    print('\n-----------------------')
    print('  Archivo enviado  ')
    print('-----------------------')

    # Recibir los datos de la imagen devuelta por el servidor
    datos_cliente = b''
    while True:
        datos = cliente.recv(1024)
        if datos:
            if datos[-5:] == b'<FIN>':
                datos_cliente += datos[:-5]
                break
            else:
                datos_cliente += datos
        else:
            break

    # Inicializamos un nuevo objeto de cifrado AES para descifrar los datos
    descifrado_cifrado = AES.new(llave, AES.MODE_EAX, sal)
    descifrado_bytes = descifrado_cifrado.decrypt(datos_cliente)

    # Comparar los datos descifrados con los datos originales de la imagen encriptada
    if descifrado_bytes == encriptado:
        print('\n-----------------------')
        print('  ¡Verificación exitosa!  ')
        print('-----------------------')
    else:
        print('\n-----------------------')
        print('  ¡Verificación fallida!  ')
        print('-----------------------')

    # Cerrar el cliente
    cliente.close()

if __name__ == "__main__":
    Main()
