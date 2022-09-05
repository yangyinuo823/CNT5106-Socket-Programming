import os
from socket import *
import time

# define the server IP and TCP Ports
# TCP Port is binded at server side
serverIP = '127.0.0.1'
serverTCP_Port = 10000
# define the client IP and UDP Port
# UDP Port is binded at client side
clientIP = '127.0.0.1'
clientUDP_Port = 6000      # used for UDP file transfer
buffer = 4096       # buffer size
Format = 'utf-8'    # format when encode and decode



def main():
    # create the TCP socket and bind it at server side
    serverTCP_Socket = socket(AF_INET, SOCK_STREAM)
    serverTCP_Socket.bind((serverIP, serverTCP_Port))
    serverTCP_Socket.listen()
    print('server running')
    # accept TCP connection requestion from client
    connection, client_addr = serverTCP_Socket.accept()


    while True:
        # receive the request command through TCP pipe
        command = connection.recv(buffer).decode(Format)
        command_list = command.split(' ')  # list command for further usage
        filelist = os.listdir('./')        # list for all files under server directory
        filelist.sort()

        # RECEIVE REQUEST 1: list all files in server folder
        if command_list[0] == 'listallfiles':
            return_data = " ".join(filelist)
            # return txt data through TCP pipe
            connection.send(return_data.encode(Format))


        # RECEIVE REQUEST 2: send a file in server folder to client
        elif command_list[0] == 'download' and command_list[1] in filelist:
            filename = command_list[1]
            # create a UDP socket
            serverUDP_Socket = socket(AF_INET, SOCK_DGRAM)
            # compute file size and number of chunks(packets)
            file_size = os.path.getsize(filename)
            num_chunks = file_size // buffer + 1
            time.sleep(0.1)
            serverUDP_Socket.sendto(str(num_chunks).encode(Format), (clientIP, clientUDP_Port))
            with open(filename, 'r') as f:
                while num_chunks:
                    chunk = f.read(buffer)
                    # increase sleep time if there's packet loss or congestion
                    time.sleep(0.002)
                    serverUDP_Socket.sendto(chunk.encode(Format), (clientIP, clientUDP_Port))
                    num_chunks -= 1
            # close the UDP socket to avoid wasting resources
            serverUDP_Socket.close()
            

        # RECEIVE REQUEST 3: send all files in server folder to client
        elif command_list[0] == 'download' and command_list[1] == 'all':
            # collect filelist and fsizelist
            fsizelist = []
            for filename in filelist:
                fsize = os.path.getsize(filename)
                fsizelist.append(str(fsize))
            files_info = "\n".join(filelist) + '@@@' + "\n".join(fsizelist)
            connection.send(files_info.encode(Format))
            # loop over filelist and send one by one
            for filename, fsize in zip(filelist, fsizelist):
                # compute number of chunks(packets) for sending
                num_chunks = int(fsize) // buffer + 1
                # sleep 0.2s to avoid TCP pipe broken
                time.sleep(0.2)
                # split the file by buffer sized chunks and send them iteratively
                with open('./' + filename, 'r') as f:
                    while num_chunks:
                        chunk = f.read(buffer)
                        connection.send(chunk.encode(Format))
                        num_chunks -= 1


        # RECEIVE REQUEST 4: exit gracefully, break out of while loop 
        elif command_list[0] == 'exit':
            break

    # close the TCP connection and TCP socket
    connection.close()   
    serverTCP_Socket.close()


if __name__ == "__main__":
    main()


        

