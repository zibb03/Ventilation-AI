import websocket
import time

ws = websocket.WebSocket()
# ws.connect("ws://192.168.0.14/")

# i = 0
# nrOfMessages = 200
#
# while i < nrOfMessages:
#     ws.send("message nr: " + str(i))
#     result = ws.recv()
#     print(result)
#     i = i + 1
#     time.sleep(1)

def sendstring(string):
    # ws = websocket.WebSocket()
    ws.connect("ws://192.168.0.14/")
    for i in range(6):
        ws.send("message nr: " + str(string[i]))
        result = ws.recv()
        print(result)

def ending():
    ws.close()

if __name__ == '__main__':
    sendstring()
    ending()