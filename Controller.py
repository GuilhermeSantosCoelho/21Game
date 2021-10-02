import hug
import json

from hug.middleware import CORSMiddleware

api = hug.API("")
api.http.add_middleware(CORSMiddleware(api))

from Cliente import *

@hug.post('/createUser')
def newUser(body=[]):
    obj = json.loads(body)
    return createUser(obj['username'])

@hug.post('/searchRooms')
def searchRooms(body=[]):
    obj = json.loads(body)
    return findRoom(obj['userId'])

@hug.post('/enterRoom')
def goRoom(body=[]):
    obj = json.loads(body)
    return enterRoom(obj['roomId'])

@hug.post('/createRoom')
def newRoom(body=[]):
    obj = json.loads(body)
    return createRoom(obj['userId'])

@hug.post('/searchRoomInfo')
def roomInfo(body=[]):
    obj = json.loads(body)
    return searchRoomInfo(obj['roomId'])

@hug.post('/startGame')
def Start(body=[]):
    obj = json.loads(body)
    return startGame(obj['roomId'])

@hug.post('/searchRoundInfo')
def roundInfo(body=[]):
    obj = json.loads(body)
    return searchRoundInfo(obj['roundId'], obj['userId'])

@hug.post('/getCard')
def card(body=[]):
    obj = json.loads(body)
    return getCard(obj['roundId'], obj['userId'])

@hug.post('/stop')
def stopCards(body=[]):
    obj = json.loads(body)
    return stop(obj['roundId'], obj['userId'])