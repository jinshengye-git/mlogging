from datetime import datetime
import psutil 
import os


class os_listener():

    def __init__(self):
        self.last_reboot_datetime = self.get_last_reboot_datetime()

    @classmethod
    def get_current_datetime(cls)->'datetime.datetime':
        #return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return datetime.now()
    @classmethod
    def get_cpu_percentage(cls)->'float':
        return psutil.cpu_percent()

    @classmethod
    def get_memory_percentage(cls)->'float':
        #python memory 
        #return 100*psutil.Process(os.getpid()).memory_info()[0]/2.**30 
        return psutil.virtual_memory()[2]

    @classmethod
    def get_thermal_fan_estimation_temperatures(cls)->'float':  
        #returns the thermal fan estimation in Celsius
        return psutil.sensors_temperatures()['thermal-fan-est'][0][1]

    @classmethod
    def get_last_reboot_datetime(cls)->'datetime.datetime':
        return datetime.fromtimestamp(psutil.boot_time())





#if __name__ == "__main__":
#    #b = os_listener()
#    a = os_listener.get_current_datetime()
#    print(a,type(a))
#    b = os_listener.get_cpu_percentage()
#    print(b,type(b))
#    c = os_listener.get_memory_percentage()
#    print(c, type(c))
#    d = os_listener.get_last_reboot_datetime()
#    print(d, type(d))
#    e = os_listener()
#
#    print(e.last_reboot_datetime)