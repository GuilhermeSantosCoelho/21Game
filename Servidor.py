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
userId = 1

def createUser(user):
	userExists = [user for user in users if user.getUsername() == user]
	print(list(users))
	if len(userExists) > 0:
		return {"success": False}
	newUser = User(user, userId)
	users.append(newUser)
	return {"success": True, "id": newUser.id}

def createRoom(user, userId):
	userHasRoom = [room for room in rooms if room.getHost() == user]
	if len(userHasRoom) > 0:
		return False
	newRoom = Room(len(rooms) + 1, user)
	newRoom.lobby.append(userId)
	rooms.append(newRoom)
	return len(rooms) + 1

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
		if createRoom(data['username'], data['userId']):
			connectionSocket.send(("Sala criada: " + str(len(rooms))).encode())
		else:
			connectionSocket.send('Não foi possível criar a sala'.encode())
   
	elif(data['action'] == 'findRoom'):
		connectionSocket.send(json.dumps(findRoom()).encode())
  
	elif(data['action'] == 'newUser'):
		userId += 1
		connectionSocket.send(json.dumps(createUser(data['username'])).encode())
  
	connectionSocket.close()