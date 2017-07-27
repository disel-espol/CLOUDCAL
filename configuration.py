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
AVERAGE_SERVICE_TIME = 0.008
MAX_AVERAGE_LATENCY = 60  #Expected response time for the request from client's perspective (in seconds)
ARRIVAL_RATE = numpy.array([
4,5,6,5,4,3,2,1.6,1.4,1.3,1.2,1.1,1,1,1.1,1.1,1.2,1.4,1.6,1.7,1.8,1.9,2,3
])


################################################
### Configurations for Reserved VMs simulations

MAX_CONCURRENT_REQUESTS_PER_VM = 2
VM_HOURLY_COST = 0.034 #Per VM hourly cost in USD


################################################
### Configurations for On-demand VMs simulations

MAX_CONCURRENT_REQUESTS_PER_VM = 2
VM_HOURLY_COST = 0.047 #Per VM hourly cost in USD


################################################
### Configurations for Serverless simulations
TIME_TO_SETUP_FUNCTION = 1.4
COST_PER_REQUEST = 0.0000002
FUNCTION_MEMORY = 128   #Compression function requires 15MB, but the minimal for billing is 128MB
COST_PER_EXECUTION = 0.00001667 #Compression function requires 0.008 secs, but usage is rounded to nearest 100m for billing.
