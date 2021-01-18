class communicator():
    def __init__(self) -> None:
        super().__init__()




class soracom(communicator):
    def __init__(self) :
        self.status = {
            'status':True,    #status: on=True, off=False
            'net_speed':'fast'#speed: 'fast', 'medium', 'slow'
        }

    def get_net_speed(self):
        # want's to give a status of network speed, function should
        # return 'fast' | 'medium' | 'slow'
        # function should collet soracom speed for 1Hz and 
        # take the average speed value as the data to judge 
        # fast, medium or slow.

        pass
