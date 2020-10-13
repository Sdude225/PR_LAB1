import socket
import json
import concurrent.futures

def tcpserver(merged_json):
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 10000))
    s.listen(5)
    print("Server is running")

    with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as ex:
        while True:
            c, addr = s.accept()
            ex.submit(receiver, c, addr, merged_json, BUFFER_SIZE)
    return

def receiver(c, addr, merged_json, BUFFER_SIZE):
    try:
        print("Connection: ", addr)
        c.sendall("select column_name/all || selectFrom column_name value\r\n".encode())
        while True:
            msg = c.recv(BUFFER_SIZE)
            if not msg:
                break
            json_query(c, msg.decode(), merged_json)
    finally:
        c.close()
    return

def json_query(c, msg, merged_json):
    query = msg.split(' ')

    if query[0] == "select":
        if query[1] == "all":
            for dictionary in merged_json:
                for item in dictionary.items():
                    c.sendall((str(item) + "\r\n").encode())
                c.sendall("\r\n".encode())
            return
        
        for dictionary in merged_json:
            for item in dictionary.items():
                if query[1] == item[0]:
                    c.sendall((str(item) + "\r\n").encode())
    
    elif query[0] == "selectFrom":
        for dictionary in merged_json:
            if query[1] in dictionary and query[2] == dictionary.get(query[1]):
                c.sendall((str(dictionary) + "\r\n").encode())

    else:
        c.sendall("\r\nInvalid query, try again\r\n".encode())
    return

