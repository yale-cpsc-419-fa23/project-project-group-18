![InstaGame Logo](/assets/instaGame_name_icon.svg)

# InstaGame

## Introduction
InstaGame is an interactive online gaming platform where users can join and play various games in real-time. It features a variety of multiplayer games, room creation options, leaderboards, and more.

## Features
- Multiplayer gaming rooms
- Real-time gameplay
- Leaderboard system
- Secure login and registration system
- Room search functionality

## Installation

To install InstaGame, follow these steps:

* Clone the repository:
   ```bash
   git clone https://github.com/yale-cpsc-419-fa23/project-project-group-18.git
   ```

### Back-end:
1. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
2. Navigate to the backend directory:
    ```bash
    cd back-end
    ```
3. Run the following command to start your backend:
    ```
    python run_server.py PORT
    ```
4. Find your backend address. After running the above command, the following address will be shown in terminal:
    ```
     * Running on all addresses (0.0.0.0)
     * Running on http://127.0.0.1:5001
     * Running on http://192.168.4.26:5001
    ```
    **IMPORTANT**: You will need to replace your backend address in the frontend ```config.js``` file.

### Front-end:
1. Navigate to the project directory:
    ```bash
    cd instaGame
    ```
2. Replace your backend address in ```config.js```:
    ```js
    export const SERVER_ADDRESS = {
    IP: YOUR_ADDRESS,
    PORT: YOUR_PORT,
    };
    ```

3. Install dependencies:
    ```bash
    npm install
    ```
4. To start the application, run the following command:
    ```bash
    npm run dev
    ```
5. Open your browser and navigate to http://localhost:xxxx
