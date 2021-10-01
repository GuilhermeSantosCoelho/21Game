from socket import *
from Entity import *
import json

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('O servidor está rodando')

rooms = []	
users = []
userId = 0

def createUser(user):
	userExists = [user for user in users if user.getUsername() == user]
	print(list(users))
	if len(userExists) > 0:
		return {"success": False}
	global userId
	userId += 1
	newUser = User(user, userId)
	users.append(newUser)
	return {"success": True, "id": newUser.id}

def userIsInRoom(userId):
	userHasRoom = [room for room in rooms if room.getHost() == userId or userId in room.lobby]
	return (len(userHasRoom) > 0)

def createRoom(userId):
	if userIsInRoom(userId):
		return {"success": False, "message": "Você já está em uma sala"}
	newRoom = Room(len(rooms) + 1, userId)
	newRoom.lobby.append(userId)
	rooms.append(newRoom)
	return {"success": True, "message": "Sala criada: " + str(len(rooms)) }

def userEnterRoom(roomId, userId):
	if userIsInRoom(userId):
		return {"success": False, "message": "Você já está em uma sala"}
	room = list(filter(lambda x: x.id == roomId, rooms))
	if len(room) > 0:
		room[0].lobby.append(userId)
		return {"success": True, "message": "Você entrou na sala", "roomId": roomId}
	return {"success": True, "message": "Sala não encontrada"}
    
def findRoom():
    returnRooms = []
    for room in rooms:
        roomInfo = room.getRoomInfo()
        user = list(filter(lambda x: x.id == roomInfo['host'], users))
        roomInfo['host'] = user[0].username
        returnRooms.append(roomInfo)
    return {"success": True, "rooms": returnRooms}

def findRoom():
    returnRooms = []
    for room in rooms:
        returnRooms.append(room.getRoomInfo())
    return returnRooms

while True:
	connectionSocket, addr = serverSocket.accept()
	data = connectionSocket.recv(1024).decode()
	data = json.loads(data)

	if(data['action'] == 'createRoom'):
		connectionSocket.send(json.dumps(createRoom(data['userId'])).encode())
   
	elif(data['action'] == 'findRoom'):
		connectionSocket.send(json.dumps(findRoom()).encode())
  
	elif(data['action'] == 'newUser'):
		connectionSocket.send(json.dumps(createUser(data['username'])).encode())
  
	elif(data['action'] == 'enterRoom'):
		connectionSocket.send(json.dumps(userEnterRoom(data['roomId'], data['userId'])).encode())
  
	connectionSocket.close()