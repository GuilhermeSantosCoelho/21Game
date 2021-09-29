from socket import *
import json
serverName = 'localhost'
serverPort = 12000

option = -1

class User:
    def __init__(self):
        self.username = ''
        
    def setUsername(self, username):
        self.username = username
    
user = User()

def createUser():
    user.username = input("Digite um nome de usuário: ")
    if len(user.username) == 0:
        print("Nome de usuário inválido")
        
def createRoom():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    if len(user.username) == 0:
        print("Nome de usuário inválido")
    else:
        clientSocket.send(json.dumps({"action": "createRoom", "username": user.username}).encode())
        returnData = clientSocket.recv(1024)
        print(returnData.decode())
    clientSocket.close()
    
def findRoom():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    if len(user.username) == 0:
        print("Nome de usuário inválido")
    else:
        clientSocket.send(json.dumps({"action": "findRoom"}).encode())
        returnData = clientSocket.recv(1024)
        print(json.loads(returnData.decode()))
    clientSocket.close()
        
while option != '0':
    print(" MENU")
    print("1 - Criar usuário")
    print("2 - Criar sala")
    print("3 - Encontrar sala")
    option = input("Digite uma opção: ")
    
    if option == '1':
        createUser()
    elif option == '2':
        createRoom()
    elif option == '3':
        findRoom()
 
# clientSocket.send(sentence.encode())
# modifiedSentence = clientSocket.recv(1024)
# print ('From Server:', modifiedSentence.decode())
# clientSocket.close()
