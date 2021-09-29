from socket import *
import json

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('O servidor está rodando')

rooms = []
colors = ['heart', 'diamonds', 'spades', 'clubs']

class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

class Room:
	def __init__(self, id, userHost):
		self.id = id
		self.userHost = userHost
		self.deck = [Card(value, color) for value in range(1, 14) for color in colors]
  
	def getHost(self):
		return self.userHost

	def resetRoom(self):
		self.deck = [Card(value, color) for value in range(1, 14) for color in colors]

def createRoom(user):
	userHasRoom = [room for room in rooms if room.getHost() == user]
	if len(userHasRoom) == 1:
		return False
	rooms.append(Room(len(rooms) + 1, user))
	return len(rooms) + 1

while True:
	connectionSocket, addr = serverSocket.accept()
	data = connectionSocket.recv(1024).decode()
	data = json.loads(data)

	if(data['action'] == 'createRoom'):
		if createRoom(data['username']):
			connectionSocket.send(("Sala criada: " + str(len(rooms))).encode())
		else:
			connectionSocket.send('Não foi possível criar a sala'.encode())
	if(data['action'] == 'findRoom'):
		connectionSocket.send(json.dumps(rooms).encode())
  
	connectionSocket.close()