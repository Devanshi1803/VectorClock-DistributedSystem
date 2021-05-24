import os
import socket
import sys
from threading import Thread
import time



def GetUdpChatMessage():
    global name
    global broadcastSocket
    global current_online
    global V 
    V = {}
    while True:
        recv_message = broadcastSocket.recv(1024)             
        recv_string_message = str(recv_message.decode('utf-8'))
        if recv_string_message.find(':') != -1:                
                    print('\r%s\n' % recv_string_message, end='')    
        elif recv_string_message.find('!@#') != -1 and recv_string_message.find(':') == -1 and recv_string_message[3:] in current_online:
            current_online.remove(recv_string_message[3:])   
            print('>> Online now: ' + str(len(current_online)))  # display the current number of peers in the network
        elif not(recv_string_message in current_online) and recv_string_message.find(':') == -1:
            current_online.append(recv_string_message)    
            print (current_online) 
            print('>> Online now: ' + str(len(current_online)))
            V.update({recv_string_message: 0})
            # V |= {recv_string_message:0}
            print (V)

def SendBroadcastMessageForChat():

    global name
    global sendSocket
    sendSocket.setblocking(False)           # do not block the socket from which broadcast messages are sent
    while True:                            
        data = input()                     
        if data == 'Exit()':               
            close_message = '!@#' + name  
            sendSocket.sendto(close_message.encode('utf-8'), ('255.255.255.255', 8080)) 
            os._exit(1)                 
        elif data != '' and data != 'Exit()':  
            send_message = name + ': '+ str(V) + data  
            sendSocket.sendto(send_message.encode('utf-8'), ('255.255.255.255', 8080))  
        else:
        
            print('Write a message first!')        


def SendBroadcastOnlineStatus():
    global name
    global sendSocket
    sendSocket.setblocking(False)           
    while True:                            
        time.sleep(1)                      
        sendSocket.sendto(name.encode('utf-8'), ('255.255.255.255', 8080))  

# main function
def main():
    global broadcastSocket
    # socket for receiving messages from peers
    broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)   
    broadcastSocket.bind(('0.0.0.0', 8080))                                
    global sendSocket
    # socket to implement sending 
    sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)          
    sendSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)       

   
    print ('*********************************************** ')

    global name
    name = ''                                                
    while True:                                                 
        if not name:
            name = input('Your name:')
            if not name:        
                print('Please enter a non-blank name!')
            else:
                break
    print('*************************************************')  

    global recvThread
    recvThread = Thread(target=GetUdpChatMessage)            

    global sendMsgThread
    sendMsgThread = Thread(target=SendBroadcastMessageForChat) 

    global current_online
    current_online = []                                      

    global sendOnlineThread
    sendOnlineThread = Thread(target=SendBroadcastOnlineStatus) 

    recvThread.start()                                        
    sendMsgThread.start()                                       
    sendOnlineThread.start()                                    
    recvThread.join()                                          
    sendMsgThread.join()                                        
    sendOnlineThread.join()                                     

if __name__ == '__main__':
    main()