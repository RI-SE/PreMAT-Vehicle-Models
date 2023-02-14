from math import cos, sin, tan

from libs import normalise_angle
from models.model import Model

from typing import Tuple


class DubinsCar(Model):

  def update(self, x: float, y: float, yaw: float, velocity: float, acceleration: float, steering_angle: float) -> Tuple[float, ...]:
    new_velocity = velocity + self.delta_time * acceleration
    angular_velocity = velocity * sin(steering_angle)
    new_x   = x + velocity*cos(yaw)*self.delta_time
    new_y   = y + velocity*sin(yaw)*self.delta_time
    new_yaw = normalise_angle(yaw + angular_velocity*self.delta_time)


    return new_x, new_y, new_yaw, new_velocity, steering_angle, angular_velocity
