"""
Configurations for Reserved Virtual Machines simulations:
"""
###################################
### Don't touch this line - import
import numpy
###################################

################################################
### General configurations, for all simualtions

START_TIME = 0  # Seconds - NOT IMPLEMENTED -> To simulate starting the experiment at a specific hour
SIMULATION_TIME = 86400 # Total simulation time (in seconds)
#AVERAGE_SERVICE_TIME = 0.008
AVERAGE_SERVICE_TIME = 0.3
#MAX_AVERAGE_LATENCY = 0.33  #Expected response time for the request from client's perspective (in seconds)
MAX_AVERAGE_LATENCY = 60

#####SYNTHETIC RATE FOR EXPERIMENTS
#ARRIVAL_RATE = numpy.array([
#4,5,6,5,4,3,2,1.6,1.4,1.3,1.2,1.1,1,1,1.1,1.1,1.2,1.4,1.6,1.7,1.8,1.9,2,3
#])

#### REAL REQUEST RATE FROM DATIL
ARRIVAL_RATE = numpy.array([
    4.745364, 6.063600, 7.923774, 10.608352, 14.594335, 20.014631, 26.161790, 28.412080, 30.432822, 30.187835,
    20.620131, 12.936782,  5.346152,  1.807029,  2.229556,  3.186768,  3.543904,  4.126800,
    4.330005,  3.319482,  3.371923,  3.806141,  3.396690,  4.052290
])

################################################
### Configurations for Reserved VMs simulations

MAX_CONCURRENT_REQUESTS_PER_VM = 2
VM_HOURLY_COST_RESERVED = 0.034 #Per VM hourly cost in USD


################################################
### Configurations for On-demand VMs simulations

MAX_CONCURRENT_REQUESTS_PER_VM = 2
VM_HOURLY_COST_ONDEMAND = 0.047 #Per VM hourly cost in USD


################################################
### Configurations for Serverless simulations
TIME_TO_SETUP_FUNCTION = 1.4
COST_PER_REQUEST = 0.0000002
FUNCTION_MEMORY = 128   #Compression function requires 15MB, but the minimal for billing is 128MB
COST_PER_EXECUTION = 0.00001667 #Compression function requires 0.008 secs, but usage is rounded to nearest 100m for billing.
