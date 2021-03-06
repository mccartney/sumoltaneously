# sumoltaneously
Issue multiple log queries towards Sumo Logic at once - i.e. sumoltaneously. 

Useful when you want to check if the scheduled search query would trigger for past data.

e.g. Run the same query for:
- 2019-12-01 12:00 - 13:40
- 2019-12-01 12:30 - 14:10
- 2019-12-01 13:00 - 14:40
- 2019-12-01 13:30 - 15:10
- ...
- 2019-12-06 12:00 - 13:40


## Usage

1. Put your query into `query.txt`
2. Specify Sumo credentials, e.g.
```
export SUMO_ACCESS_ID="susomething"
export SUMO_ACCESS_KEY="zsomething"
export SUMO_ENDPOINT="https://api.sumologic.com/api/v1"
```
3. Edit `run.py` for prefered startTime, etc.
4. `run.py` e.g.
```
PYTHONUNBUFFERED=TRUE python3.6 run.py | tee /tmp/my.precious.output
```

## Future ideas

- run towards multiple orgs
