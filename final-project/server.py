import socket
from _thread import *
import pickle
from game import Game

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            msg = conn.recv(4096)
            data = pickle.loads(msg)

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data['action'] == "reset":
                        game.resetWent()
                        if p == 0:
                            game.toggle_turn()
                        game.reset_game()
                    elif data['action'] != "get":
                        if data['action'] == "move":
                            game.play(p, int(data['message']))
                        elif data['action'] == "choice":
                            game.select(int(data['message']))
                        elif data['action'] == "lock":
                            game.lock(data['player'])

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].connect = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))