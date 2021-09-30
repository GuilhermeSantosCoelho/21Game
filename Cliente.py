from socket import *
from Entity import *
import json
serverName = 'localhost'
serverPort = 12000

option = -1
user = None


def createUser():
    username = input("Digite um nome de usuário: ")
    if len(username) == 0:
        print("Nome de usuário inválido")
    else:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        clientSocket.send(json.dumps(
            {"action": "newUser", "username": username}).encode())
        returnData = json.loads(clientSocket.recv(1024).decode())
        print(returnData)
        if returnData['success']:
            global user
            user = User(username, returnData['id'])
        clientSocket.close()


def createRoom():
    if not user:
        print("Você precisa criar um usuário")
    else:
        print(user)
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        clientSocket.send(json.dumps(
            {"action": "createRoom", "username": user.username, "userId": user.id}).encode())
        returnData = clientSocket.recv(1024)
        print(returnData.decode())
        clientSocket.close()


def findRoom():
    if not user:
        print("Você precisa criar um usuário")
    else:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        clientSocket.send(json.dumps({"action": "findRoom"}).encode())
        returnData = clientSocket.recv(1024)
        roomsReturned = json.loads(returnData.decode())
        print("SALAS DISPONÍVEIS:")
        for room in roomsReturned:
            print("SALA", room['id'], "- Dono: ", room['host'],
                  "- Pessoas na sala: ", len(room['lobby']))
        clientSocket.close()

        roomNumber = input("Selecione qual sala deseja entrar: ")
        enterRoom(roomNumber)


def enterRoom(roomNumber):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(json.dumps({"action": "enterRoom", "roomId": roomNumber, "userId": user.id}).encode())
    print("todo")


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
