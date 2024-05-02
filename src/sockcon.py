import socket 

def socketTransmit(socketIP, socketPort): 
    UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try: 
        message = "<U1> $ Chan 1 full full #".encode('utf-8')
        UDPsocket.sendto(message, (socketIP, socketPort))
        print("Command sent...")
    except Exception as e: 
        print("Error: ", e)
    finally: 
        print("Socket closed...")
        UDPsocket.close()

def socketRecieve(socketIP, socketPort): 
    UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try: 
        while True: 
            message = ""
            status = UDPsocket.recv_into(message)
            if status == 0: 
                print(message.decode())
            
    except Exception as e: 
        print("Error: ", e)
    finally: 
        print("Socket close...")
        UDPsocket.close()
            

def main(): 
    socketTransmit("172.16.64.126", 4000)

if __name__ == "__main__": 
    main()

