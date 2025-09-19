import socketserver
import json
from datetime import datetime
import http.server

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def handle(self):
        try:
            data = self.request.recv(1024).decode('utf-8')
            response = self.process_command(data)
            self.request.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            self.request.sendall(json.dumps({"error": str(e)}).encode('utf-8'))

    def get_time(self):
        response = {
            "timestamp": datetime.now().isoformat(),
            "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return json.dumps(response, indent=4)

    def get_ping(self):
        response = {
            "status": "pong",
            "timestamp": datetime.now().isoformat(),
            "message": "server MIGHT be running but idk (heavy on the MIGHT) -- all systems are running lol"
        }
        return json.dumps(response, indent=4)

    def get_help(self):
        help_info = {
            "commands": {
                "get_time": "get the current time",
                "ping": "get a ping response",
                "help": "you get this message"
            },
            "description": "send any command to get a json response"
        }
        return json.dumps(help_info, indent=4)

    def process_command(self, data):
        try:
            command = data.strip()
            if command == "time":
                return self.get_time()
            elif command == "ping":
                return self.get_ping()
            elif command == "help":
                return self.get_help()
                # ADD YOUR COMMANDS HERE THEN DEFINE THEM AT THE TOP (below get_help preferably + add them to the help message)
            else:
                return json.dumps({"error": "that command doesn't exist"})
        except Exception as e:
            return json.dumps({"error": str(e)})


class Server:
    def __init__(self, host='0.0.0.0', port=8000):
        self.host = host
        self.port = port
        self.server = None 

    def start(self):
        try:
            self.server = socketserver.TCPServer((self.host, self.port), RequestHandler)
            print(f"Server started on {self.host}:{self.port}\nYou can use the commands: PING, TIME, HELP \nTo stop the server, use CTRL+C")
            self.server.serve_forever() 

        except KeyboardInterrupt:
            print("\nServer stopped")
            self.stop()
            
        except Exception as e:
            print(f"Error: {e}")

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None

if __name__ == "__main__":
    server = Server()
    server.start()


        

"""
Todo list:
1. make a web interface / move away from json
2. add these commands:
- server info
- ip
- uptime
- cpu usage
- memory usage
- network usage
3. how to connect it to cardputer??? i think there's an ssh thingy for that but i really cannot remember...maybe also figure out how to get tailscale on there and have this all on a tailnet w/ the cardputer when it's connected to the internet? i should probably google it.
"""