from models.model import Model
from models.bicycle_model import BicycleModel
from models.dubins_car import DubinsCar


class ModelFactory:

  def __init__(self, wheelbase: float, max_steer: float, delta_time: float=0.05):
    self.wheelbase = wheelbase
    self.max_steer = max_steer
    self.delta_time = delta_time


  def create_model(self, model_type: str):
    if (model_type == "BicycleModel"):
      return BicycleModel(self.wheelbase, self.max_steer, self.delta_time)
    elif (model_type == "DubinsCar"):
      return DubinsCar(self.wheelbase, self.max_steer, self.delta_time)

