#!/usr/bin/python

import os
import time
import datetime
from sumologic import SumoLogic

sumo = SumoLogic(os.environ["SUMO_ACCESS_ID"], os.environ["SUMO_ACCESS_KEY"], os.environ["SUMO_ENDPOINT"])

# --------------- INPUT 

with open("query.txt", "r") as query_file:
  query = query_file.read()

duration = 160 * 60 * 1000
startTimeStep = 30 * 60 * 1000

firstStartTime = 1574636400000
lastStartTime = 1575241200000

runCount = int((lastStartTime - firstStartTime) / startTimeStep)

# ---------------------

def startQuery(iteration):
  thisStartTime = firstStartTime + iteration * startTimeStep
  return sumo.search_job(query, fromTime = thisStartTime, toTime = thisStartTime + duration, timeZone = "CET", byReceiptTime = False)

def dateForIteration(iteration):
  return datetime.datetime.fromtimestamp((firstStartTime + iteration * startTimeStep) / 1000).strftime("%m/%d/%Y %I:%M %p")

waitingForResults = {}
maxConcurrentQueries = 10
iterationsToRun = list(range(0, runCount))
readyResults = {}

print("The following iterations will need to be performed: %s" %(iterationsToRun))

while iterationsToRun or waitingForResults:
  # check already started runs
  iterationsToBeRemoved=[]
  for iteration, waiting in waitingForResults.items():
    status = sumo.search_job_status(waiting)
    if status['state'] == 'DONE GATHERING RESULTS':
      print("Iteration %d ready, saving results" % (iteration))
      readyResults[iteration] = status
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
  if result['recordCount'] > 0:
    print("%4d %20s -> resultCount: %d" %(iteration, 
      dateForIteration(iteration),
      result['recordCount']))
    