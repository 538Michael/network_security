from socket import *
import ssl

server = socket(AF_INET, SOCK_STREAM)
server.bind(('127.0.0.1', 4444))
server.listen(2)

print("Server rodando...")

while True:
    obj, addr = server.accept()

    server_ssl = ssl.wrap_socket(
        obj,
        server_side=True,
        certfile="./cert.pem",
        keyfile="./key.pem",
        ssl_version=ssl.PROTOCOL_TLSv1
    )

    try:
        while server_ssl:
            message = server_ssl.read()

            if message:
                print(message)
    except:
        server_ssl.close()
        obj.close()            