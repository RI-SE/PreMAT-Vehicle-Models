from math import cos, sin, tan

from libs import normalise_angle
from models.model import Model

from typing import Tuple


class BicycleModel(Model):


    def update(self, x: float, y: float, yaw: float, velocity: float, acceleration: float, steering_angle: float) -> Tuple[float, ...]:
        """
        Summary
        -------
        Updates the vehicle's state using the kinematic bicycle model

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
        
        friction_road = 0.0 
        friction_air = 0.0

        # Compute the local velocity in the x-axis
        friction = velocity * (friction_road + friction_air)
        new_velocity = velocity + self.delta_time * (acceleration - friction)

        # Limit steering angle to physical vehicle limits
        steering_angle = -self.max_steer if steering_angle < -self.max_steer else self.max_steer if steering_angle > self.max_steer else steering_angle

        # Compute the angular velocity
        angular_velocity = new_velocity*tan(steering_angle) / self.wheelbase

        # Compute the final state using the discrete time model
        new_x   = x + velocity*cos(yaw)*self.delta_time
        new_y   = y + velocity*sin(yaw)*self.delta_time
        new_yaw = normalise_angle(yaw + angular_velocity*self.delta_time)
        
        return new_x, new_y, new_yaw, new_velocity, steering_angle, angular_velocity
