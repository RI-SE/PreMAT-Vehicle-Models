class Model:
    
    def __init__(self, wheelbase: float, max_steer: float, delta_time: float=0.05):

        self.delta_time = delta_time
        self.wheelbase = wheelbase
        self.max_steer = max_steer