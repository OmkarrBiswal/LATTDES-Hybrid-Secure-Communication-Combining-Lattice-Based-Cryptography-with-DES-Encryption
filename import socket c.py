import socket
from itertools import product
from Crypto.Cipher import DES

def des_decrypt(cipher_text, key):
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.decrypt(cipher_text).rstrip(b' ')

def brute_force_message(encrypted_message):
    print("Trying all possible keys")
    for key in product(range(256), repeat=8):
        key_bytes = bytes(key)
        cipher_text = des_decrypt(encrypted_message, key_bytes)
        try:
            decrypted_message = cipher_text.decode('utf-8').rstrip('\x00')
            return decrypted_message
        except UnicodeDecodeError:
            pass

    return "Brute force failed! Unable to decrypt the message."

def client_program():
    host = 'localhost'
    port = 5000  # socket server port number
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024)  # receive response
        print('Received from server: ' + data.decode())  # show in terminal

        follow_up = input(" -> ")
        if follow_up == "DECRYPT":
            client_socket.send("ENCRYPT".encode())
            key = client_socket.recv(8)
            client_socket.send(f"DATA:{data.hex()}".encode())
            decrypted_data = client_socket.recv(1024)
            print("Decrypted data:", decrypted_data.decode('utf-8'))
        elif follow_up == "BRUTE":
            decrypted_message = brute_force_message(data)
            print(decrypted_message)

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection

if __name__ == '__main__':
    client_program()