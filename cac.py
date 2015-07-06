# Socket server in python using select function

import socket, select
import os

if __name__ == "__main__":

    CONNECTION_LIST = []    # list of socket clients
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print "Command and Controle Server started on port " + str(PORT)

    def checkforCommands(data):

        GetCommand = data

        if GetCommand == "test\r\n":
            print "[\033[32m Bot CaC Check Succsessfully\033[0m ] "
            sock.send('CaC : Check was Successfull.')
            sock.send('\n')
        if GetCommand == "exit\r\n":
            sock.close()
            CONNECTION_LIST.remove(sock)
            print "[\033[31m Bot (%s, %s) is offline\033[0m ]" % addr
        if GetCommand == "ifconfig\r\n":
            Status = os.system("ifconfig | grep en1")
            #sock.send('Status :' + Status)
            print Status




    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

        for sock in read_sockets:

            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "[\033[32m Bot (%s, %s) connected\033[0m ]" % addr

            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    # echo back the client message
                    if data:
                        sock.send('Bot :  ' + data)
                        checkforCommands(data)

                # client disconnected, so remove from socket list
                except:
                    broadcast_data(sock, "Bot (%s, %s) is offline" % addr)
                    print "[\033[31m Bot (%s, %s) is offline\033[0m ]" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()
