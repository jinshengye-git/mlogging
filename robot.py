class robot():
    def __init__(self):
        self.robot_status = 0 # 0: normal,  1: error,  2: standby

class keycart(robot):
    def __init__(self):
        self.battery_percentage = 1.0 # 100%
        self.pin_status = 0 # 0:up, 1:down
        self.error_codes = -1 # -1 : no error codes,  1 -- 99
        self.led_info = (0,1) # (color, status).  color: 0 = yellow, 1 = red; 
                       # status = 0,1,2,3;  (off/on/flash 0.5/flash 2.0)
        self.melody_phone_status = (1,0) #(melody_phone1_status, melody_phone2_status)
                        # melody_phone1_status: 0 = on, 1 = off
                        # melody_phone2_status: 0 = driving, 1 = alarm
        self.lcd_emergency_button = 0
        self.break = 0 #0 = free, 1 = break
        self.motor_info = ((0,0),(0,0)) # (left_motor_info,  right_motor_info)
                    # left_motor_info: (
                    #       status(0=normal,1=error), speed(0=normal,1=too much)
                    # )  
                    # right_motor_info: (
                    #       status(0=normal,1=error), speed(0=normal,1=too much)
                    #)
    
    def get_battery_percentage(self):
        pass
        #self.battery_percentage = 0.0

    def get_pin_status(self):
        pass

    