from socket import *
from random import randint
colors = ['heart', 'diamonds', 'spades', 'clubs']


class User:
    def __init__(self, username, id):
        self.id = id
        self.username = username

    def setUsername(self, username):
        self.username = username

    def getUsername(self):
        return self.username


class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color


class Room:
    def __init__(self, id, userHost):
        self.id = id
        self.userHost = userHost
        self.lobby = []
        self.deck = []
        self.roundId = 0

    def getHost(self):
        return self.userHost

    def resetRoom(self):
        self.deck = [Card(value, color) for value in range(1, 14) for color in colors]

    def getRoomInfo(self):
        return {"id": self.id, "host": self.userHost, "lobby": self.lobby, "roundId": self.roundId}
    
    def getCardFromDeck(self):
        indexRandom = randint(0, len(self.deck) - 1)
        card = self.deck[indexRandom]
        del self.deck[indexRandom]
        return card


class Round:
    def __init__(self, id, actualPlayer):
        self.id = id
        self.actualPlayer = actualPlayer
        self.playersCards = []
        self.playersPoints = []
        self.winner = ''
        self.isLastPlayer = False
        self.gameFinished = False

    def getRoundInfo(self, userId):
        cards = []
        for card in self.playersCards:
            if card['userId'] == userId or self.gameFinished:
                cards.append({"card": card, "userId": userId})
            else:
                cards.append({"card": '-', "userId": card['userId']})
        return {"id": self.id, "actualPlayer": self.actualPlayer, "cards": cards, "finished": self.gameFinished, "winner": self.winner}
    
    def getCard(self, userId, card):
        self.playersCards.append({"userId": userId, "cardValue": card.value, "cardColor": card.color})

class MySocket():
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def Connect(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def Disconnect(self):
        self.socket.close()

    def Send(self, data):
        self.Connect()
        self.socket.send(data)
        returnedData = self.socket.recv(1024).decode()
        self.Disconnect()
        return returnedData
