import socket
from Crypto.Cipher import AES

def Main():
    host = "localhost"
    port = 5000
    address = (host, port)
    buff = 2048

    # Generamos la llave (16 bytes) y tipo de encriptación
    llave = b'Esta_es_mi_llave'
    sal = b'Esta_es_mi_-sal-'
    cifrado = AES.new(llave, AES.MODE_EAX, sal)

    # Establecemos el socket utilizando TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(address)
    servidor.listen()
    print('\n************************')
    print('  Esperando archivo...  ')
    print('************************')

    # Acepta la conexión y el socket de un cliente
    cliente, cliente_add = servidor.accept()

    archivo_nombre = "imagen_nueva.jpg"

    # Abrimos el archivo para escritura en modo binario
    with open(archivo_nombre, 'wb') as archivo:
        terminado = False
        archivo_bytes = b''

        # Descargamos los datos de la imagen
        while not terminado:
            datos = cliente.recv(buff)
            if datos:
                # Revisamos los últimos 5 bytes enviados
                if datos[-5:] == b'<FIN>':
                    terminado = True
                    archivo_bytes += datos[:-5]
                else:
                    archivo_bytes += datos
            else:
                break

        descifrado_bytes = cifrado.decrypt(archivo_bytes)
        archivo.write(descifrado_bytes)

    print('\n-----------------------')
    print('  ¡Archivo recibido!  ')
    print('-----------------------')
    print('-- Nombre del archivo:', archivo_nombre, ' --')

    # Leer los datos del archivo recibido en el servidor
    with open(archivo_nombre, 'rb') as archivo_servidor:
        datos_servidor = archivo_servidor.read()

    # Enviar los datos de la imagen nuevamente al cliente
    cliente.sendall(datos_servidor)

    # Esperar una respuesta del cliente para asegurarse de que ha recibido los datos
    cliente.settimeout(5)
    try:
        cliente.recv(1)
    except socket.timeout:
        pass

    # Cerrar el cliente y el servidor
    cliente.close()
    servidor.close()

if __name__ == "__main__":
    Main()
