import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("localhost", 3000)
print("Starting Server...")
try:
    sock.bind(server_address)
except:
    print("Server Already Started")
    exit()

if __name__ == "__main__":
    chats = {}
    messages = {}

    sock.listen(4)
    while True:
        connection, client_address = sock.accept()
        print(f"Connection to {client_address}")
        messages[client_address] = ""
        while True:
            portion = connection.recv(8)
            print(portion)
            if portion:
                decoded_portion = portion.decode('utf-8')
                messages[client_address] += decoded_portion
            else:
                print("Got '"+messages[client_address]+"'")
                break
