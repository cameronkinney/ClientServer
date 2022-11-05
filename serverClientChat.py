import socket
import threading

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8000  # The port used by the server

# Sender
class ChatSender(threading.Thread):

    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    def run(self):
        while (True):
            message = input(": ")

            # Checking if we are sending file
            if message.startswith("Send"):
                self.sendfile(self.connection, message.split(" ")[1])

            self.connection.sendall(message.encode())
    # Sending file
    def sendfile(self, connection, file_name):
        header = str("Send " + file_name)
        connection.send(header.encode())

        # Open in read byte mode
        file = open(file_name, 'rb')

        # Read the file
        data = file.read(1024)

        # Send data
        while (data):
            connection.send(data)
            data = file.read(1024)

        file.close()
        return


# Receives a file
# New file is created when opening
def recievefile(self, file_name):
    # Create new file with sent added to the end of the filename
    # Open in write byte mode
    file = open(str(file_name + "sent"), 'wb')

    # Receive data and write to file (broken)
    while (data := self.connection.recv(1024)):
        # if data == b'1':
        #     break
        # Test print
        print("data:", data)
        file.write(data)
        # data = self.connection.recv(1024)

    file.close()
    return


# Listener
class ChatListener(threading.Thread):
    def __init__(self, connection, prefix):
        threading.Thread.__init__(self)
        self.prefix = prefix
        self.connection = connection

    def run(self):
        while (True):
            # Read in bytes
            read_bytes = self.connection.recv(1024)

            # Decoding message in utf-8
            message = (read_bytes.decode("utf-8"))

            # Listening for Send command
            if message.startswith("Send"):
                recievefile(self, message.split(" ")[1])

                # Informing a file was sent
                full = str(self.prefix + " Sent a file.")
                print(full)
            else:
                full = str(self.prefix + message)
                print(full)


class Chat:
    def __init__(self, client):

        # Connect to the HOST and PORT defined at start of file
        # Communication between server and client
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if client:
                s.connect((HOST, PORT))
                # Initialize sender and listener
                sender = ChatSender(s)
                listener = ChatListener(s, "Server :")

                # Start chat threads
                sender.start()
                listener.start()
            else:
                s.bind((HOST, PORT))
                s.listen()
                connection, addr = s.accept()

                sender = ChatSender(connection)
                listener = ChatListener(connection, "Client :")

                # Start chat threads
                sender.start()
                listener.start()

            while (True):
                continue
