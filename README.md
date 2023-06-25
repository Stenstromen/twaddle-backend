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
