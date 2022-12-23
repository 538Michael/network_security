from socket import *
import ssl

client = socket(AF_INET, SOCK_STREAM)
client_ssl = ssl.wrap_socket(client,ciphers="AES256-GCM-SHA384", ca_certs="./cert.crt")

client_ssl.connect(('127.0.0.1', 4444))

while True:
    message = input("Mensagem : ")

    if message:
        client_ssl.write(message.encode())

#client.close()
