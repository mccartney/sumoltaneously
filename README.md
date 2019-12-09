# sumoltaneously
Issue multiple log queries towards Sumo Logic at once - i.e. sumoltaneously. 

Useful when you want to check if the scheduled search query would trigger for past data.


## Usage

1. Put your query to `query.txt`
2. `run.py` e.g.
```
PYTHONUNBUFFERED=TRUE python3.6 run.py | tee /tmp/my.precious.output
```

## Future ideas

- run towards multiple orgs
