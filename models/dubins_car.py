from math import cos, sin, tan

from libs import normalise_angle
from models.model import Model

from typing import Tuple


class DubinsCar(Model):

  def update(self, x: float, y: float, yaw: float, velocity: float, acceleration: float, steering_angle: float) -> Tuple[float, ...]:
    """
        Summary
        -------
        Updates the vehicle's state using the Dubins Car model

        Parameters
        ----------
        x (int) : vehicle's x-coordinate [m]
        y (int) : vehicle's y-coordinate [m]
        yaw (int) : vehicle's heading [rad]
        velocity (int) : vehicle's velocity in the x-axis [m/s]
        acceleration (int) : vehicle's accleration [m/s^2]
        steering_angle (int) : vehicle's steering angle [rad]

        Returns
        -------
        new_x (int) : vehicle's x-coordinate [m]
        new_y (int) : vehicle's y-coordinate [m]
        new_yaw (int) : vehicle's heading [rad]
        new_velocity (int) : vehicle's velocity in the x-axis [m/s]
        steering_angle (int) : vehicle's steering angle [rad]
        angular_velocity (int) : vehicle's angular velocity [rad/s]
        """
    
    new_velocity = velocity + self.delta_time * acceleration
    angular_velocity = velocity * sin(steering_angle)
    new_x = x + velocity*cos(yaw)*self.delta_time
    new_y = y + velocity*sin(yaw)*self.delta_time
    new_yaw = normalise_angle(yaw + angular_velocity*self.delta_time)


    return new_x, new_y, new_yaw, new_velocity, steering_angle, angular_velocity
