# Real-time Chat Room Application

A real-time chat room application built with FastAPI and WebSocket technology. This application allows multiple users to communicate in real-time through a web interface.

## Features

- Real-time messaging using WebSocket connections
- Clean and responsive user interface
- Message history persistence during active sessions
- User join notifications
- Support for emoji messages
- Cross-Origin Resource Sharing (CORS) enabled

## Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn
- WebSocket support in your browser

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install the required dependencies:
```bash
pip install fastapi uvicorn
```

## Running the Application

1. Start the server:
```bash
uvicorn main:app --reload
```

2. Open your web browser and navigate to:
```
http://localhost:8000
```

3. Enter your name when prompted to join the chat room.

## How to Use

1. When you first open the application, you'll be prompted to enter your name
2. Once connected, you can start sending messages
3. Messages from all connected users will appear in real-time
4. The chat history will be visible to new users who join the room
5. You can use emojis in your messages

## Technical Details

- Built with FastAPI framework
- Uses WebSocket for real-time communication
- Implements a ConnectionManager class to handle WebSocket connections
- Includes CORS middleware for cross-origin requests
- Features a responsive HTML/CSS/JavaScript frontend

## Project Structure

```
├── main.py          # Main application file containing FastAPI routes and WebSocket logic
└── README.md        # This documentation file
```

## Security Considerations

- The application currently allows all origins (`*`) for CORS
- In a production environment, you should restrict CORS to specific origins
- Consider implementing user authentication for production use

## License

This project is open source and available under the MIT License. 
