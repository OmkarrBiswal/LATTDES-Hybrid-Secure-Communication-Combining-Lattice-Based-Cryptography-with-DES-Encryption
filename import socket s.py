import socket
from Crypto.Cipher import DES
import os

def newhope_key_exchange():
    return os.urandom(8)  # Simulated key exchange

def des_encrypt(plain_text, key):
    cipher = DES.new(key, DES.MODE_ECB)
    while len(plain_text) % 8 != 0:
        plain_text += b' '
    return cipher.encrypt(plain_text)

def des_decrypt(cipher_text, key):
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.decrypt(cipher_text).rstrip(b' ')

def server_program():
    host = 'localhost'
    port = 5000  # port to listen on
    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("From connected user: " + data)
        if data == "ENCRYPT":
            shared_secret = newhope_key_exchange()
            conn.send(shared_secret)
        elif data.startswith("DATA:"):
            _, encrypted_data = data.split(":", 1)
            encrypted_data = bytes.fromhex(encrypted_data)
            key = conn.recv(8)  # Receive the key after data
            decrypted_data = des_decrypt(encrypted_data, key)
            print("Decrypted data:", decrypted_data.decode('utf-8'))
            conn.send(decrypted_data)
        else:
            shared_secret = newhope_key_exchange()
            encrypted_data = des_encrypt(data.encode('utf-8'), shared_secret)
            conn.send(encrypted_data.hex().encode('utf-8'))  # send encrypted data as hex

    conn.close()  # close the connection

if __name__ == '__main__':
    server_program()