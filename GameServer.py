import socket
import selectors
import sys
import types

HOST = '127.0.0.1'
PORT = 65432
sel = selectors.DefaultSelector()

numberOfPlayersString = sys.argv[1]
numberOfPlayers = int(numberOfPlayersString[16:])
numberOfSnakesString = sys.argv[2]
numberOfSnakes = int(numberOfSnakesString[15:])
PlayerSockets = []

print("Server starting. Number of players: {0}. Number of snakes per each player: {1}".format(int(numberOfPlayers),
                                                                                              int(numberOfSnakes)))
# Server logic


def accept_wrapper(sock):  # Accepting clients and making sockets non-blocking
    conn, addr = sock.accept()
    print("Player connected from address: ", addr)
    print("Player got ID: ", len(PlayerSockets))

    sts = "{0};{1};{2}".format(numberOfPlayers, numberOfSnakes, len(PlayerSockets))
    conn.sendall(sts.encode())
    conn.setblocking(False)  # We dont wanna players to block our server
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE  # Players will send/receive data to/from sever
    sel.register(conn, events, data=data)
    PlayerSockets.append(conn)


def service_connection(key, mask):  # Handling incoming msgs from clients
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:  # If we have something to receive from clients
        recv_data = sock.recv(1024)  # Receive
        if recv_data:
            data.outb += recv_data  # add to buffer
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:  # If clients are ready to receive commands from server
        if data.outb:  # if there is un send commands send them to remaining clients
            print("Sending command to clients: ", repr(data.outb))
            for i in range(len(PlayerSockets)):
                if PlayerSockets[i] != sock:  # We wont send command to player who made a move
                    sent = PlayerSockets[i].send(data.outb)
                    data.outb = data.outb[sent:]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while len(PlayerSockets) < numberOfPlayers:  # waiting for all players to connect
        accept_wrapper(s)

    for sck in PlayerSockets:
        sts = "GO"
        sck.sendall(sts.encode())
    """while True:
        events = sel.select(timeout=None)  # sel.select(timeout=None) blocks until there are sockets ready for I/O.
        for key, mask in events:
            service_connection(key, mask)"""

