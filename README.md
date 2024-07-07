
# LoL Esports API

## Overview

This project is a containerized Flask application that provides an API for retrieving League of Legends Esports data. The backend is built using Flask and Flask-RESTX, and it interacts with the Esports data through the `mwrogue` library. The frontend is assumed to be a Node.js application.

## Project Structure

```
your_project/
│
├── backend/
│   └── test/
│       ├── app.py
│       ├── config.py
│       ├── Dockerfile
│       ├── esports_client.py
│       ├── models.py
│       ├── requirements.txt
│       ├── routes.py
│       ├── services.py
│
├── frontend/
│   ├── serveur.js
│
├── app.py
├── docker-compose.yml
```

### Backend

- `app.py`: The main entry point of the Flask application.
- `config.py`: Configuration settings (if any).
- `esports_client.py`: Setup for the Esports client.
- `models.py`: API models.
- `routes.py`: API endpoints/routes.
- `services.py`: Business logic and helper functions.
- `Dockerfile`: Instructions to containerize the backend.
- `requirements.txt`: Python dependencies for the backend.

### Frontend

- `serveur.js`: The main entry point of the Node.js application.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

```sh
git clone https://github.com/WessimH/DashBoard.git
cd your_project
```

2. Build and run the Docker containers:

```sh
docker-compose build
docker-compose up
```

The backend Flask application should now be running on `http://localhost:5000` and the frontend on `http://localhost:3000`.

## API Endpoints

### Draft Information

#### GET `/api/esports/drafts/<patch>`

Retrieves draft information for a specific patch.

**Parameters:**
- `patch` (string): The patch identifier.

**Response:**

```json
[
    {
        "Team1Role1": "role1",
        "Team1Role2": "role2",
        ...
    },
    ...
]
```

### Champion Statistics

#### GET `/api/esports/champion_stats`

Retrieves statistics for champions for a given patch.

**Parameters:**
- `patch` (query parameter, required): The patch version to filter matches.
- `champion` (query parameter, optional): The champion name to filter statistics.

**Response:**

```json
[
    {
        "champion": "ChampionName",
        "role": "Role",
        "games_played": 10,
        "winrate": 50.0,
        "blue_side_avg_pick_pos": 2.1,
        "red_side_avg_pick_pos": 3.2,
        "blue_side_pick_pct": 60.0,
        "red_side_pick_pct": 40.0
    },
    ...
]
```

## Development

### Backend Development

To develop the backend, navigate to the `backend/test` directory and make your changes. You can run the Flask application locally by using the following commands:

```sh
cd backend/test
pip install -r requirements.txt
flask run
```

### Frontend Development

To develop the frontend, navigate to the `frontend` directory and make your changes. You can run the Node.js application locally by using the following commands:

```sh
cd frontend
npm install
node serveur.js
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

