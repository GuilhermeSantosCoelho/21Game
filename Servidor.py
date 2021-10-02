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
rounds = []
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
	return {"success": True, "message": "Sala criada: " + str(len(rooms)), "roomId": len(rooms)}

def userEnterRoom(roomId, userId):
	if userIsInRoom(userId):
		return {"success": False, "message": "Você já está em uma sala"}
	room = list(filter(lambda x: x.id == roomId, rooms))
	if len(room) > 0:
		room[0].lobby.append(userId)
		return {"success": True, "message": "Você entrou na sala", "roomId": roomId}
	return {"success": False, "message": "Sala não encontrada"}
    
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
    return {"success": True, "rooms": returnRooms}

def roomInfo(roomId):
	room = list(filter(lambda x: x.id == roomId, rooms))
	if len(room) > 0:
		players = []
		for userId in room[0].lobby:
			user = list(filter(lambda x: x.id == userId, users))
			players.append({"id": userId, "name": user[0].getUsername()})
		return {"success": True, "info": room[0].getRoomInfo(), "players": players}
	return {"success": False, "message": "Sala não encontrada"}

def roundInfo(roundId, userId):
	round = list(filter(lambda x: x.id == roundId, rounds))
	if len(round) > 0:
		return {"success": True, "info": round[0].getRoundInfo(userId)}
	return {"success": False, "message": "Ocorreu um erro"}

def getCard(roundId, userId):
	round = list(filter(lambda x: x.id == roundId, rounds))
	if len(round) > 0:
		room = list(filter(lambda x: x.roundId == roundId, rooms))
		round[0].getCard(userId, room[0].getCardFromDeck())
		return {"success": True}
	return {"success": False, "message": "Ocorreu um erro"}

def stop(roundId, userId):
	round = list(filter(lambda x: x.id == roundId, rounds))
	if len(round) > 0:
		room = list(filter(lambda x: x.roundId == roundId, rooms))
		if round[0].isLastPlayer:
			round[0].gameFinished = True
			finishGame(room[0], round[0])
			return 
		nextPlayer = list(filter(lambda x: x != round[0].actualPlayer, room[0].lobby))
		getCard(round[0].id, nextPlayer[0])
		getCard(round[0].id, nextPlayer[0])
		round[0].actualPlayer = nextPlayer[0]
		round[0].isLastPlayer = True
		return {"success": True}
	return {"success": False, "message": "Ocorreu um erro"}

def finishGame(room, round):
	players = room.lobby
	for player in players:
		playerCards = list(filter(lambda x: x['userId'] == player, round.playersCards))
		points = 0
		for card in playerCards:
			if(card['cardValue'] > 10):
				points += 10
			else:
				points += card['cardValue']
		round.playersPoints.append({"userId": player, "points": points})

	if round.playersPoints[0]['points'] == round.playersPoints[1]['points']:
		round.winner = 'Empate'
		return

	if round.playersPoints[0]['points'] > 21 and round.playersPoints[1]['points'] > 21:
		if round.playersPoints[0]['points'] < round.playersPoints[1]['points']:
			user = list(filter(lambda x: x.id == round.playersPoints[0]['userId'], users))
			round.winner = user[0].getUsername()
		else:
			user = list(filter(lambda x: x.id == round.playersPoints[1]['userId'], users))
			round.winner = user[0].getUsername()
	elif round.playersPoints[0]['points'] > 21 or round.playersPoints[1]['points'] > 21:
		if round.playersPoints[0]['points'] < round.playersPoints[1]['points']:
			user = list(filter(lambda x: x.id == round.playersPoints[0]['userId'], users))
			round.winner = user[0].getUsername()
		else:
			user = list(filter(lambda x: x.id == round.playersPoints[1]['userId'], users))
			round.winner = user[0].getUsername()
	else:
		if round.playersPoints[0]['points'] > round.playersPoints[1]['points']:
			user = list(filter(lambda x: x.id == round.playersPoints[0]['userId'], users))
			round.winner = user[0].getUsername()
		else:
			user = list(filter(lambda x: x.id == round.playersPoints[1]['userId'], users))
			round.winner = user[0].getUsername()

def startGame(roomId):
	room = list(filter(lambda x: x.id == roomId, rooms))
	if len(room) > 0:
		room[0].resetRoom()
		userId = newRound(room[0].lobby)
		room[0].roundId = len(rounds)
		getCard(len(rounds), userId)
		getCard(len(rounds), userId)
		return {"success": True, "roundId": len(rounds)}

def newRound(lobby):
    indexRandom = randint(0,1)
    rounds.append(Round(len(rounds) + 1, lobby[indexRandom]))
    return lobby[indexRandom]

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
  
	elif(data['action'] == 'roomInfo'):
		connectionSocket.send(json.dumps(roomInfo(data['roomId'])).encode())
  
	elif(data['action'] == 'startGame'):
		connectionSocket.send(json.dumps(startGame(data['roomId'])).encode())
  
	elif(data['action'] == 'roundInfo'):
		connectionSocket.send(json.dumps(roundInfo(data['roundId'], data['userId'])).encode())
  
	elif(data['action'] == 'getCard'):
		connectionSocket.send(json.dumps(getCard(data['roundId'], data['userId'])).encode())
  
	elif(data['action'] == 'stop'):
		connectionSocket.send(json.dumps(stop(data['roundId'], data['userId'])).encode())
  
	connectionSocket.close()