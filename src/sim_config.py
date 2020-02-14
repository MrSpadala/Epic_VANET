 
import os
import json


class config:
	# Here are reported the default configuration values
	# 
	# DO NOT MODIFY THIS, modify sim_parameters.json file instead 
	# 

	# Simulation parameters
	ncpus = 1                  #how many cores to use
	nsimulations = 4           #how many simulations to perform
	time_resolution = 0.0001   #discretized time resolution

	# Environment parameters
	Tmax = 0.1      #max time to wait before sending a broadcast message
	Tmin = 0        #min time to wait before sending a broadcast message
	Rmin = 170      #Rmin, expressed in meters
	Rmax = 500	    #Rmax, expressed in meters
	drop = 0.01	    #message drop rate
	alpha = 0.05    #if at the end of the waiting timer, a fraction larger than ALPHA
					#of my neighors has not been reached I relay the message

	# Connectivity graph
	city_name = "Luxembourg"
	scenario = "time27100Tper1000.txt"
	
	# Cologne
	# city_name = "Cologne"
	# scenario = "time23000Tper1000.txt"

	# New York
	# city_name = "NewYork"
	# scenario = "Newyork5003.mat"

	# Use CBF algorithm instead of EPIC
	use_CBF = False
	# If use_CBF is True, then this variable represent the number of messages a vehicle
	# has to receive during the waiting in order to not relay a message. 
	# If use_CBF is False this is not used.
	CBF_msg_thresh = 1


def _json_encode(file_out):
	d = config.__dict__
	to_encode = {k:v for k,v in d.items() if not (k.startswith("__") and k.endswith("__"))}
	json.dump(to_encode, file_out, indent=4)

def _json_decode(file_in):
	d = json.load(file)
	for k,v in d.items():
		setattr(config, k, v)


if not os.path.isfile("sim_parameters.json"):
	with open("sim_parameters.json", "w") as file:
		_json_encode(file)


with open("sim_parameters.json", "r") as file:
	_json_decode(file)

