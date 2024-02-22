# Twaddle-Backend

## Set Python3 environment

```bash
python3 -m venv twaddlevenv
source twaddlevenv/bin/activate
```

## Install requirements

```bash
python3 -m pip install -r requirements.txt
```

## Start

```bash
AUTHORIZATION_KEY="lol" \
CORS_ORIGINS="http://localhost:5173" \
python3 app.py
```

## `Socket.IO` Client Emit

/generate

```bash
{
   "input":"Hello, world!",
   "max_length": 120
}
```

## `Socket.IO` Server Emit

/generated

```bash
{
   "output":"[The next GPT2 token word]" 
}
```

## Docker

```bash
docker run --rm \
-e CORS_ORIGINS="*" \
-e AUTHORIZATION_KEY="lol" \
-p80:8080 \
-v $PWD/models/:/app/models \
ghcr.io/stenstromen/twaddle-backend:latest
```
