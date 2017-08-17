"""
"""
import random
import simpy
from math import trunc
#from math import ceil
import numpy

from configuration import *  

ARRIVAL_RATE = 1/ARRIVAL_RATE
ARRIVAL_RATE *= 8
MAX_RATE = max(ARRIVAL_RATE)

SERVICE_TIME_SUM = 0.0
TIME_IN_THE_SYSTEM_SUM = 0.0
SERVICE_TIME_COUNT = 0

#latency = numpy.array([])
latency = []
latency_peak = []


def source(env, interval, counter, avg_service_time):
    CURRENT_HOUR = 0
    CURRENT_ARRIVAL_SUM = 0.0
    CURRENT_ARRIVAL_COUNT = 0
    """Source generates customers randomly"""
    i=0
    pthinning = [(1-hourlyrate/MAX_RATE) for hourlyrate in ARRIVAL_RATE]

    while env.now <= interval:
        i+=1
        c = customer(env, 'Request%02d' % i, counter, avg_service_time)
        env.process(c)

        uthin=0.0
        pthin=1.0
        t = env.now
        t_old = t

        while (uthin < pthin):
            deltat = random.expovariate(MAX_RATE)
            t = t + deltat
            pthin = pthinning[trunc(t/3600) % 24]
            uthin = random.random()        
        new_hour = trunc(t/3600) % 24
        if new_hour > CURRENT_HOUR:
            print('Average rate: %d, %f' % (CURRENT_HOUR, CURRENT_ARRIVAL_COUNT/CURRENT_ARRIVAL_SUM))
            #print('SUM, COUNT: %f, %d' % (CURRENT_ARRIVAL_SUM,CURRENT_ARRIVAL_COUNT))
            CURRENT_HOUR = new_hour
            CURRENT_ARRIVAL_COUNT = 0
            CURRENT_ARRIVAL_SUM = 0.0
        CURRENT_ARRIVAL_SUM += t-t_old
        CURRENT_ARRIVAL_COUNT += 1
        yield env.timeout(t-t_old)
    print('Average rate: %d, %f' % (CURRENT_HOUR, CURRENT_ARRIVAL_COUNT/CURRENT_ARRIVAL_SUM))
        
def customer(env, name, counter, avg_service_time):
    global SERVICE_TIME_SUM, SERVICE_TIME_COUNT, TIME_IN_THE_SYSTEM_SUM, latency
    """Customer arrives, is served and leaves."""
    arrive = env.now
    #print('%7.4f %s: Here I am' % (arrive, name))

    with counter.request() as req:
        # Wait for the counter or abort at the end of our tether
        yield req 

        wait = env.now - arrive

        # Customer request start being served
        #print('%7.4f %s: Waiting Time: %7.4f' % (env.now, name, wait))

        service_time = random.expovariate(1.0 / avg_service_time) + TIME_TO_SETUP_FUNCTION
        SERVICE_TIME_SUM += service_time
        SERVICE_TIME_COUNT += 1
        yield env.timeout(service_time)
        #print('%7.4f %s: Serving Time: %7.4f' % (env.now, name, service_time))
        #print('%7.4f %s: Finished - Time on the System: %7.4f' % (env.now, name, wait+service_time))
        TIME_IN_THE_SYSTEM_SUM += wait+service_time
        #latency = numpy.append(latency,wait+service_time)
        latency.append(wait+service_time)
        if (trunc(env.now/3600) % 24) == 12 :
            latency_peak.append(wait+service_time)

############ MAIN FUNCTION
print('Starting Simulations:')
print
SERVICE_TIME_SUM = 0.0
SERVICE_TIME_COUNT = 0

#random.seed(RANDOM_SEED)
env = simpy.Environment(initial_time=START_TIME)

# Start processes and run
counter = simpy.Resource(env, capacity=float('inf'))
env.process(source(env, SIMULATION_TIME, counter, AVERAGE_SERVICE_TIME))

startTime = env.now
env.run()
print('Simulation Time: %7.4f' % (env.now-startTime))
print('Average Service Time: %7.4f' % (SERVICE_TIME_SUM/SERVICE_TIME_COUNT))
average_latency = numpy.average(latency)
print('Average Time in the System: %7.4f' % average_latency)
# Print results
print('=====================')
print('=====================')
print('=====================')
print('RESULTS:')
print
print('Max. Required Latency: %7.4f' % MAX_AVERAGE_LATENCY)
print('Average Latency: %7.4f' % numpy.average(latency))
if numpy.average(latency) > MAX_AVERAGE_LATENCY:
    print('WARNING!!! Average Latency is exceeding the user\'s SLO')
print('90th Percentile Latency: %7.4f' % numpy.percentile(latency,90))
print('99th Percentile Latency: %7.4f' % numpy.percentile(latency,99))
monthly_request = 31 * SERVICE_TIME_COUNT 
request_cost = 0
if monthly_request > 1000000:
    request_cost = (monthly_request - 1000000) * COST_PER_REQUEST

computing_time = monthly_request * (round(((SERVICE_TIME_SUM/SERVICE_TIME_COUNT)-TIME_TO_SETUP_FUNCTION) * 10) / 10) * FUNCTION_MEMORY / 1024
computing_cost = 0
if computing_time > 400000:
    computing_cost = (computing_time - 400000) * COST_PER_EXECUTION
#print('Yearly cost: %7.4f' % (365*24*reserved_vms*VM_HOURLY_COST))
print('=====================')
print('Monthly requests: %d' % monthly_request)
print('Monthly Request Cost: %7.2f' % request_cost)
print('Monthly Computing Cost: %7.2f' % computing_cost)
print('Yearly Cost: %7.2f' % (12 * (request_cost + computing_cost)))

## Print Latencies  - ENABLE ONLY FOR DEBUG
#for v in latency_peak: print v