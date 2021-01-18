from posix import POSIX_FADV_NOREUSE
from serial import Serial, serialutil
from rospy import ServiceException, Subscriber
import sensor
from obstacle_msgs.msg import sensors_range

from mymath.my_math import severity



class ultrasonic(sensor):
    
	def __init__(self,**kwargs):
		#self._namespace = kwargs.get('namespace','/')
		#self._topic = self._namespace + 'ultrasonic_distance_array_msgs'
		#self.subscriber=None
        #try:
		#	self.subscriber = Subscriber(self._topic, sensors_range ,self._sensor_data)
        #except ServiceException as exc:
        #    # report a complain of no service from ros.
        #    print("Service did not process request: " + str(exc))
        #    pass
		#self.sensor_name=kwargs.get('sensorname') #'FC' 'FL' 'FR' 'SL' 'SR'
		# check  /dev/ttyACM0  5 sensor are all
		# on one opencm...
		# one of them disconnect will not cause 
		self.usb_on = True                          
		self.sensor_msg = {
			'sensor0':{'obs_detect': True, 'obs_dist': 0.0},
			'sensor1':{'obs_detect': True, 'obs_dist': 0.0},
			'sensor2':{'obs_detect': True, 'obs_dist': 0.0},
			'sensor3':{'obs_detect': True, 'obs_dist': 0.0},
			'sensor4':{'obs_detect': True, 'obs_dist': 0.0}
		}	
		#overall reliabilits 
		self.reliability = {
			'sensor0':(0.0, 0.0, 0.0),	# sensor 0 (usb_on, obs_det, obs_dist)
			'sensor1':(0.0, 0.0, 0.0),	# sensor 1 (usb_on, obs_det, obs_dist)
			'sensor2':(0.0, 0.0, 0.0),	# sensor 2 (usb_on, obs_det, obs_dist)
			'sensor3':(0.0, 0.0, 0.0),	# sensor 3 (usb_on, obs_det, obs_dist)
			'sensor4':(0.0, 0.0, 0.0)	# sensor 4 (usb_on, obs_det, obs_dist)
		}
		#probability of failure		
		self.prob_failure = {
			'sensor0':(0.0, 0.0, 0.0),	# sensor 0 (usb_on, obs_det, obs_dist)
			'sensor1':(0.0, 0.0, 0.0),	# sensor 1 (usb_on, obs_det, obs_dist)
			'sensor2':(0.0, 0.0, 0.0),	# sensor 2 (usb_on, obs_det, obs_dist)
			'sensor3':(0.0, 0.0, 0.0),	# sensor 3 (usb_on, obs_det, obs_dist)
			'sensor4':(0.0, 0.0, 0.0)	# sensor 4 (usb_on, obs_det, obs_dist)
		}

		self.thrs_reliab = (1.0, 1.0, 1.0) # (usb_on, obs_det, obs_dist)
		
		#probability of failure thresholds
		self.thrs_prob_failure = (0.8, 0.8, 0.8)# (usb_on, obs_det, obs_dist)		
		
		self.temp_log = {
			'usb': (None,None,None,None,None,None,None,None,None,None),#T / F 
			'sensor0': (  # last 10 data on log
				(None,None,None,None,None,None,None,None,None,None),#obs_detect
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),#obs_distance
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),#fail prob
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) #reliability
			),
			'sensor1': (  # last 10 data on log
				(None,None,None,None,None,None,None,None,None,None),#obs_detect
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),#obs_distance
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),#fail prob
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) #reliability
			),
			'sensor2': (  # last 10 data on log
				(None,None,None,None,None,None,None,None,None,None),#obs_detect
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),#obs_distance
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),#fail prob
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) #reliability
			),
			'sensor3': (  # last 10 data on log
				(None,None,None,None,None,None,None,None,None,None),#obs_detect
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),#obs_distance
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),#fail prob
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) #reliability
			),
			'sensor4': (  # last 10 data on log
				(None,None,None,None,None,None,None,None,None,None),#obs_detect
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),#obs_distance
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),#fail prob
				(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) #reliability
			)
		}
		self.severity = 1.0 # 1. normal,   3. failed.

	def check_usb(self):
        
        #    currently can not import monitoring pkg in my python code directly,
        #    therefore, I similarly make a function like 
        #    monitoring/src/hardware/ultrasonic.py 
        #    to check the USB connection of opencm
        #    , another way is to check the monitoring log and read the 
		#	 usb status from there ~/.log/seaos .
        # The way reading from the log file needs to confirm from keycart 
		# but I think a log file recording line by line (block by block)
		# and I read the latest line from the file, and get the data I want.
		
		# the way from OS : by monitoring pkg, Authors: Tim Fronsee 
        try:
            opencm_port = Serial('/dev/ttyACM0', timeout=1)	
            # Don't read if another process is using the serial port.
            if not opencm_port.isOpen():
                opencm_port.read()
                opencm_port.close()
            self.usb_on = True
        
        except serialutil.SerialException:
            self.usb_on = False
            self.is_error = True #sensor class.

	def sensor_data(self, msgs: sensors_range):
    	
    	# Callback function for /ultrasonic_distance_array_msgs topic.
    	
    	sonicsensors = []
    	for msg in msgs.data:
        	asonic = {'obstacle': False,
                  'frame_id': msg.header.frame_id,
                  'range': msg.range}
        	sonicsensors.append(asonic)

	def set_reliability(self,vals = (0.0,0.0,0.0)):
		self.reliability = vals

	def reset_prob_failure(self):
		self.prob_failure = (0.0,0.0,0.0)

	def update_overall_reliability(self,val_name,pre_val,val,threshold,step): 
		pass


	def update_pf_rb(self):
		
		usb_connection = False
		probability_threshold = 1.0
		failure_prob = 0.0
		uid = 'FC' #FC, FL， FR， SL， SR
		a = 0.15
		b = 0.2
		obs_dist = 0.25
		obs_detect = True
		reliability = 0.0
		
		

		if usb_connection:
			if obs_dist >=0.25 and obs_dist <=4.5:
				if uid == 'FC':
					#pass
					if obs_dist<=0.8:
						a, b = None
						
					else:
						a, b = None
				elif (uid == 'FR' or uid == 'FL'):
					if obs_dist <= 0.57 :
					#pass
						a, b = None
					else :
						a, b = None
				elif (uid == 'SR' or uid == 'SL'):
					#pass
					if obs_dist <=0.35 :
						a, b = None
					else :
						a, b = None

				else:
					print("Please check uid, it must be one of FC,FR,FL,SR,SL.")				

				#use a, b
				reliability = (obs_dist *a+b) * reliability
				
				#update the failure probability.
				a_ = 0.15
				failure_prob = failure_prob - a_
				if(failure_prob>=probability_threshold):
					print("Ultrasonic sensor [%s] is failure".format(uid))
				elif(failure_prob <= a_):
					failure_prob = 0.0
				else:
					failure_prob = failure_prob - a_


			elif obs_dist == 0.0:
				a_ = 0.3
				failure_prob = failure_prob + a_
				reliability = (1.0-failure_prob) * reliability
			else:
				# define a, b 
				reliability = (obs_dist*a+b)*reliability



		else:

			b_ = 0.3
			failure_prob = b_ + failure_prob
			if(failure_prob >= probability_threshold):
				print("Ultrasonic sensor [%s] is failure".format(uid))
				reliability = 0.0
			else:
				reliability = (1-failure_prob)*reliability


		
		
		

										
		
		
		
		
		
		
		
		
				
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		





	def logging(self):
		#when failure happens report 
		# a status value
		# an error message
		
		pass
