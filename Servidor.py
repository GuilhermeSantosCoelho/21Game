from socket import *
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('O servidor está rodando')
# while True:
# 	connectionSocket, addr = serverSocket.accept()
# 	sentence = connectionSocket.recv(1024).decode()
# 	capitalizedSentence = sentence.upper()
# 	connectionSocket.send(capitalizedSentence.encode())
# 	connectionSocket.close()


class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

colors = ['heart', 'diamonds', 'spades', 'clubs']


def InitializeRound():
    deck = [Card(value, color) for value in range(1, 14) for color in colors]
    print(len(deck))


InitializeRound()