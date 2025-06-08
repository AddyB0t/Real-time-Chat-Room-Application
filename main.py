from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Store active connections and message history
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.message_history: List[str] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # Send message history to new client
        for message in self.message_history:
            await websocket.send_text(message)
        await self.broadcast(f"A new user joined the chat")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        self.message_history.append(message)
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def get():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat Room</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f0f2f5;
            }
            .chat-container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                padding: 20px;
            }
            #messages {
                height: 400px;
                overflow-y: auto;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 20px;
                background: #fff;
            }
            .message {
                margin: 10px 0;
                padding: 10px;
                border-radius: 5px;
                background: #e9ecef;
            }
            #message-form {
                display: flex;
                gap: 10px;
            }
            #message-input {
                flex: 1;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
            }
            button {
                padding: 10px 20px;
                background: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <h1>Chat Room</h1>
            <div id="messages"></div>
            <form id="message-form">
                <input type="text" id="message-input" placeholder="Type your message (emojis allowed!)..." autocomplete="off">
                <button type="submit">Send</button>
            </form>
        </div>

        <script>
            let username = "";
            while (!username) {
                username = prompt("Enter your name to join the chat:");
                if (username) {
                    username = username.trim();
                }
            }

            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
            
            const messages = document.getElementById('messages');
            const messageForm = document.getElementById('message-form');
            const messageInput = document.getElementById('message-input');

            ws.onopen = function() {
                console.log('Connected to WebSocket');
            };

            ws.onerror = function(error) {
                console.error('WebSocket error:', error);
            };

            ws.onclose = function() {
                console.log('Disconnected from WebSocket');
            };

            ws.onmessage = function(event) {
                const message = document.createElement('div');
                message.className = 'message';
                message.textContent = event.data;
                messages.appendChild(message);
                messages.scrollTop = messages.scrollHeight;
            };

            messageForm.onsubmit = function(e) {
                e.preventDefault();
                const message = messageInput.value;
                if (message) {
                    ws.send(`[${username}]: ${message}`);
                    messageInput.value = '';
                }
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except:
        manager.disconnect(websocket)

