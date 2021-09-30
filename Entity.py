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
		self.deck = [Card(value, color) for value in range(1, 14) for color in colors]

	def getHost(self):
		return self.userHost

	def resetRoom(self):
		self.deck = [Card(value, color) for value in range(1, 14) for color in colors]

	def getRoomInfo(self):
		return {"id": self.id, "host": self.userHost, "lobby": self.lobby}