import socket
from Crypto.Cipher import AES

def Main():
    host = "localhost"
    port = 5000
    address = (host, port)
    buff = 1024

    # Generamos la llave(16 bytes) y tipo de encriptación
    llave = b'Esta_es_mi_llave'
    sal = b'Esta_es_mi_-sal-'
    cifrado = AES.new(llave, AES.MODE_EAX, sal)

    # Establecemos el socket, utilizando TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(address)
    servidor.listen()
    print('\n************************')
    print('  Esperando archivo...  ')
    print('************************')

    # Acepta la conexion y socket de un cliente
    cliente, cliente_add = servidor.accept()

    archivo_nombre = cliente.recv(buff).decode()

    # Abrimos la imagen para escritura y definimos
    # cuando se acaba de transmitir el tamaño de la imagen
    archivo = open(archivo_nombre, 'wb')
    terminado = False
    archivo_bytes = b''

    # Descargamos los datos de la imagen
    while not terminado:
        datos = cliente.recv(buff)
        # Revisamos los últimos 5 bytes enviados
        if archivo_bytes[-5:] == b'<FIN>':
            terminado = True
        else:
            archivo_bytes += datos

    archivo.write(cifrado.decrypt(archivo_bytes[:-5]))
    print('\n-----------------------')
    print('  ¡Archivo recibido!  ')
    print('-----------------------')
    print('-- Nombre del archivo:', archivo_nombre,' --')

    # Cerramos el archivo y los sockets
    archivo.close()
    cliente.close()
    servidor.close()

if __name__ == "__main__":
    Main()
