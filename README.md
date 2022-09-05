# CNT5106-Socket-Programming

course project for computer networks CNT5106C\
Programming language: Python

### Project requirements
- **$ listallfiles** (Request message to be typed in the client process’ terminal)
  - Requirement: List all files in server process' current directory: Text containing the list of files must be sent via TCP. The server’s listing of files must be sent to the client, but then the client process must output (print) that complete listing of files on the client’s terminal

- **$ download filename** (Request message to be typed in the client process’ terminal)
  - Requirement: Download one file from the server process' current directory by name: Copy of the correct file must be sent via UDP only and stored in the client’s current directory
  - Note: I did this through UDP transfer. To avoid packet loss and congestion, I add time.sleep(0.002) for each packet sending iteration. It may take a little bit longer time to transfer for a large file.

- **$ download all** (Request message to be typed in the client process’ terminal)
  - Requirement: Download all files from the server process' current directory: Copy of the correct files must be sent using either TCP or UDP and stored in the client’s current directory
  - Note: I did this through TCP transfer

- **$ exit** (Request message to be typed in the client process’ terminal)
  - Requirement: Graceful termination of the client and server applications by properly closing any open sockets

