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