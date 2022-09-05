from socket import *
import time
import os

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
    # create the TCP socket and connect to server
    clientTCP_Socket = socket(AF_INET, SOCK_STREAM)
    clientTCP_Socket.connect((serverIP, serverTCP_Port))

    

    while True:
        # input the request command
        command = input('> ')
        command_list = command.split(' ')

        # SEND REQUEST 1: list all files in server folder
        if command_list[0] == 'listallfiles':
            # send request command and receive messages by TCP pipe
            clientTCP_Socket.send(command.encode(Format))
            message = clientTCP_Socket.recv(buffer).decode(Format)
            print(message)


        # SEND REQUEST 2: download a file with its name from server folder
        elif command_list[0] == 'download' and command_list[1] != 'all':
            # create UDP listening socket to further file receive
            clientUDP_Socket = socket(AF_INET, SOCK_DGRAM)
            clientUDP_Socket.bind((clientIP, clientUDP_Port))
            # send the request command by TCP pipe
            clientTCP_Socket.send(command.encode(Format))
            # receive file by chunks through UDP socket
            filename = command_list[1]
            if os.path.exists('./' + filename):
                os.remove('./' + filename)
            num_chunks, server_addr = clientUDP_Socket.recvfrom(buffer)
            num_chunks = int(num_chunks.decode(Format))
            # write new file from sent data
            with open('./' + filename, 'w') as f:
                while num_chunks:
                    chunk, server_addr = clientUDP_Socket.recvfrom(buffer)
                    chunk = chunk.decode(Format)
                    f.write(chunk)
                    num_chunks -= 1
            # close the UDP socket to avoid wasting resources
            clientUDP_Socket.close()
            print(f'Downloaded {filename}')


        # SEND REQUEST 3: download all files from server folder
        elif command_list[0] == 'download' and command_list[1] == 'all':
            # send request command by TCP pipe
            clientTCP_Socket.send(command.encode(Format))
            # receive files_info by TCP pipe
            file_info = clientTCP_Socket.recv(buffer).decode(Format)
            filelist, fsizelist = file_info.split("@@@")
            filelist = filelist.split('\n')
            fsizelist = fsizelist.split('\n')
            # loop over filelist and receive files one by one
            for filename, fsize in zip(filelist, fsizelist):
                if os.path.exists('./' + filename):
                    # remove existing same file to avoid overwrite issue
                    os.remove('./' + filename)
                # computer number of chunks(packets) for the file
                num_chunks = int(fsize) // buffer + 1
                # write new files from sent data
                with open('./' + filename, 'w') as f:
                    while num_chunks:
                        chunk = clientTCP_Socket.recv(buffer).decode(Format)
                        f.write(chunk)
                        num_chunks -= 1
                        
            print('Downloaded all')
            
        

        # SEND REQUEST 4: exit gracefully
        elif command_list[0] == 'exit':
            clientTCP_Socket.send(command.encode(Format))
            break
    
    # close the TCP socket
    clientTCP_Socket.close()


if __name__ == "__main__":
    main()



        
