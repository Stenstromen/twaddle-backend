# Twaddle-Backend

## Set Python3 environment
```
python3 -m venv twaddlevenv
source twaddlevenv/source/activate
```

## Install requirements
```
python3 -m pip install -r requirements.txt
```

## Start
```
AUTHORIZATION_KEY="lol" \
CORS_ORIGINS="http://localhost:5173" \
python3 gpt2.py
```

## Post request
```
/generate
{
   "input":"Hello, world!"
}
```

## JSON response
```
/generate
{
   "output":"[The next GPT2 token word]" 
}
```

## Docker 
```
docker run --rm \
-e CORS_ORIGINS="*" \
-e AUTHORIZATION_KEY="lol" \
-p80:80 \
-v $PWD/models/:/app/models \
twaddletest:latest
```