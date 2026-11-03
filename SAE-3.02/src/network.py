import socket
import json
import threading


class Server:
    def __init__(self):
        self.running = True
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.socket.bind(("127.0.0.1", 5000))
        self.socket.listen(5)

    def start(self):
        thread = threading.Thread(target=self.listen,daemon=True)
        thread.start()

    def listen(self):
        while self.running:
            try:
                client, address = (self.socket.accept())
                thread = threading.Thread(target=self.handle,args=(client,),daemon=True)
                thread.start()
            except OSError:
                break

    def handle(self, client):
        try:
            data = client.recv(1024)
            if not data:
                return
            message = json.loads(data.decode())
            print("Message reçu :",message)
            response = {"status": "ok"}
            client.send(json.dumps(response).encode())
        except (json.JSONDecodeError,OSError):
            response = {"status": "error"}
            try:
                client.send(json.dumps(response).encode())
            except OSError:
                pass
        finally:
            client.close()

    def stop(self):
        self.running = False
        try:
            self.socket.close()
        except OSError:
            pass

def send_message(message):
    try:
        sock = socket.create_connection(("127.0.0.1", 5000),timeout=2)
        sock.send(json.dumps(message).encode())
        response = sock.recv(1024)
        sock.close()
        return json.loads(response.decode())
    except (OSError,json.JSONDecodeError):
        return None