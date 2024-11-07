#!/usr/bin/python

import os
import time
import datetime
from sumologic import SumoLogic

sumo = SumoLogic(os.environ["SUMO_ACCESS_ID"], os.environ["SUMO_ACCESS_KEY"], os.environ["SUMO_ENDPOINT"])

# --------------- INPUT 

with open("query.txt", "r") as query_file:
  query = query_file.read()

duration = 24 * 60 * 60 * 1000
startTimeStep = 10 * 24 * 60 * 60 * 1000

firstStartTime = 1704067200000
lastStartTime = 1730419200000

runCount = int((lastStartTime - firstStartTime) / startTimeStep)

# ---------------------

def startQuery(iteration):
  thisStartTime = firstStartTime + iteration * startTimeStep
  return sumo.search_job(query, fromTime = thisStartTime, toTime = thisStartTime + duration, timeZone = "Europe/Warsaw", byReceiptTime = False)

def dateForIteration(iteration):
  return datetime.datetime.fromtimestamp((firstStartTime + iteration * startTimeStep) / 1000).strftime("%m/%d/%Y %I:%M %p")

waitingForResults = {}
maxConcurrentQueries = 10
iterationsToRun = list(range(0, runCount))
readyResults = {}
print("The following iterations will need to be performed: %s" %("\n".join(list(map(dateForIteration, iterationsToRun)))))

while iterationsToRun or waitingForResults:
  # check already started runs
  iterationsToBeRemoved=[]
  for iteration, waiting in waitingForResults.items():
    status = sumo.search_job_status(waiting)
    if status['state'] == 'DONE GATHERING RESULTS':
      print("Iteration %d ready, saving results" % (iteration))
      readyResults[iteration] = (status, sumo.search_job_records(waiting, limit =1))
      iterationsToBeRemoved.append(iteration)
  for iteration in iterationsToBeRemoved: del(waitingForResults[iteration])
  
  # start new if possible
  while (len(waitingForResults) < maxConcurrentQueries) and iterationsToRun:
    iteration = iterationsToRun.pop()
    print("Starting query execution for iteration %d" % (iteration))
    waitingForResults[iteration] = startQuery(iteration)
    time.sleep(1)
  
  time.sleep(10)  

print("The results are ready: %s" % (len(readyResults)))
print("Non-zero results: ")
for iteration, result in sorted(readyResults.items()):
  if result[0]['recordCount'] > 0:
    fields = result[1]["fields"]
    firstValues = {field["name"]:result[1]["records"][0]["map"][field["name"]] for field in fields}
    print("%4d %20s -> resultCount: %d, 1st result: %s" %(iteration,
      dateForIteration(iteration),
      result[0]['recordCount'],
      firstValues,
      ))
    