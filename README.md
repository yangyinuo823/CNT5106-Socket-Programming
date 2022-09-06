# CNT5106-Socket-Programming

course project for computer networks CNT5106C\
Programming language: Python
Project time: 2022 Apr

### How to use it
- use a terminal to run ```python server.py``` in server directory
- use another terminal to run ``` python client.py``` in client directory
- under client terminal, use commands:
  - ```$ listallfiles``` 
    - List all files in server process' current directory via TCP
  - ```$ download filename```
    - Download one file from the server process' current directory by name via UDP
    - To avoid packet loss and congestion, I add time.sleep(0.002) for each packet sending iteration. It may take a little bit longer time to transfer for a large file.
  - ```$ download all```
    - Download all files from the server process' current directory via TCP
  - ```$ exit```
    - Graceful termination of the client and server applications by properly closing any open sockets


