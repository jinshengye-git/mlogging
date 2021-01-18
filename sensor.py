class sensor():
    def __init__(self):
        self.power_on = True
        self.is_sensing = True
        self.is_error = False

class velodyne(sensor):
    def __init__(self):
        self.lan_connect = True
        self.ip_check = True
        
class camera(sensor):
	def __init__(self):
		self.usb_on = True
		self.streaming = True

















































































