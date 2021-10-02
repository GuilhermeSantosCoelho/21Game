from socket import *
from Entity import *
import json
serverName = 'localhost'
serverPort = 12000

option = -1
user = None
mySocket = MySocket('localhost', 12000)

def createUser(username):
    if len(username) == 0:
        {"success": False, "message": "Nome de usuário inválido"}
    else:
        returnData = json.loads((mySocket.Send(json.dumps({"action": "newUser", "username": username}).encode())))
        if returnData['success']:
            global user
            user = User(username, returnData['id'])
        return returnData


def createRoom(userId):
    if not userId:
        return {"success": False, "message": "Você precisa criar um usuário"}
    else:
        return json.loads(mySocket.Send(json.dumps({"action": "createRoom", "userId": userId}).encode()))

def findRoom(userId):
    if not userId:
        return {"success": False, "message": "Você precisa criar um usuário"}
    else:
        return json.loads(mySocket.Send(json.dumps({"action": "findRoom"}).encode()))

def enterRoom(roomNumber):
    return json.loads(mySocket.Send(json.dumps({"action": "enterRoom", "roomId": int(roomNumber), "userId": user.id}).encode()))

def searchRoomInfo(roomNumber):
    return json.loads(mySocket.Send(json.dumps({"action": "roomInfo", "roomId": int(roomNumber)}).encode()))

def searchRoundInfo(roundId, userId):
    return json.loads(mySocket.Send(json.dumps({"action": "roundInfo", "roundId": int(roundId), "userId": int(userId)}).encode()))

def getCard(roundId, userId):
    return json.loads(mySocket.Send(json.dumps({"action": "getCard", "roundId": int(roundId), "userId": int(userId)}).encode()))

def stop(roundId, userId):
    return json.loads(mySocket.Send(json.dumps({"action": "stop", "roundId": int(roundId), "userId": int(userId)}).encode()))

def startGame(roomNumber):
    return json.loads(mySocket.Send(json.dumps({"action": "startGame", "roomId": int(roomNumber)}).encode()))

if __name__ == "__main__":
    while option != '0':
        print(" MENU")
        print("1 - Criar usuário")
        print("2 - Criar sala")
        print("3 - Encontrar sala")
        option = input("Digite uma opção: ")

        if option == '1':
            username = input("Digite um nome de usuário: ")
            returnData = createUser(username)
            if returnData['success']:
                print("Usuário criado")
            else:
                print("Falha ao criar usuário")
        elif option == '2':
            returnData = createRoom(user.id)
            if returnData['success']:
                print("Sala criada")
            else:
                print("Falha ao criar sala")
        elif option == '3':
            returnData = findRoom(user.id)
            print("SALAS DISPONÍVEIS:")
            for room in returnData['rooms']:
                print("SALA", room['id'], "- Dono: ", room['host'], "- Pessoas na sala: ", len(room['lobby']))
            roomNumber = input("Selecione qual sala deseja entrar: ")
            roomData = enterRoom(roomNumber)
            print(roomData['message'])

# clientSocket.send(sentence.encode())
# modifiedSentence = clientSocket.recv(1024)
# print ('From Server:', modifiedSentence.decode())
# clientSocket.close()
