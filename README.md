# pokedex_uncc

## Current Project Structure:
```
├── docker-compose.yml
├── pokemon_data.json
├── types/
│   └── [type images (.png files)]
├── frontend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── streamlit_app.py
└── backend/
    ├── Dockerfile
    ├── main.py
    └── requirements.txt
```

## Commands:
### 1. Running docker container/app in detached mode
```
docker-compose up -d --build
```
Build the frontend and backend images, Start both services


### 2.1 Stop the app and delete containers
```
docker-compose down
```

Stops and removes running containers, Keeps images and volumes

### 2.2 Stop the app without deleting containers
```
docker-compose stop
```
This stops containers and keeps them around so they can be restarted with:

```
docker-compose start
```

### 3.1 Cleaning Up Docker (Optional), by removing all containers
```
docker container prune
```

### 3.2 Clean Up Docker (Optinal), by removing all unused images
```
docker image prune
```

## Access:
use localhost instead of 0.0.0.0