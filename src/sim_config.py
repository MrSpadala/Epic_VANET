 
import os
import json


DEFAULT_CONFIG = {
    # Simulation parameters
    "ncpus": 1,                  #how many cores to use
    "nsimulations": 4,           #how many simulations to perform
    "time_resolution": 0.0001,   #discretized time resolution

	# Environment parameters
	"Tmax": 0.3,      #max time to wait before sending a broadcast message
	"Tmin": 0,        #min time to wait before sending a broadcast message
	"Rmin": 170,      #Rmin, expressed in meters
	"Rmax": 500,	    #Rmax, expressed in meters
	"drop": 0.01,	    #message drop rate
	"alpha": 0.05    #if at the end of the waiting timer, a fraction larger than ALPHA
					#of my neighors has not been reached I relay the message
}


if not os.path.isfile("sim_parameters.json") and False:
    with open("sim_parameters.json", "w") as file:
        json.dump(DEFAULT_CONFIG, file, indent=4)


with open("sim_parameters.json", "r") as file:
    d = json.load(file)
    print(d)



