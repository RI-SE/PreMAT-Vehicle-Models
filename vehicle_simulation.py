from simulation_info import Simulation, Car, Path, Fargs, animate
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np

class VehicleSimulation:
    def __init__(self, data: str, model: str, vmax: float, constant_velocity: bool = False):
        self.path = Path(data)
        self.sim  = Simulation(self.path.delta_time, max_size_x = 5, max_size_y = 5, frames = len(self.path.acceleration))
        self.car  = Car(self.path.px[0], self.path.py[0], self.path.pyaw[0],
                        self.path.px, self.path.py, self.path.pyaw, self.path.acceleration,
                        self.path.delta_time, self.path.time[-1], vmax, model, constant_velocity)


    def show_animation(self):
        path = self.path
        sim = self.sim
        car = self.car

        interval = sim.dt * 10**3

        fig = plt.figure()
        ax = plt.axes()
        ax.set_aspect('equal')

        ax.plot(path.px, path.py, '--', color='gold')

        empty              = ([], [])
        target,            = ax.plot(*empty, '+r')
        car_outline,       = ax.plot(*empty, color=car.colour)
        front_right_wheel, = ax.plot(*empty, color=car.colour)
        rear_right_wheel,  = ax.plot(*empty, color=car.colour)
        front_left_wheel,  = ax.plot(*empty, color=car.colour)
        rear_left_wheel,   = ax.plot(*empty, color=car.colour)
        rear_axle,         = ax.plot(car.x, car.y, '+', color=car.colour, markersize=2)
        annotation         = ax.annotate(f'{car.x:.1f}, {car.y:.1f}', xy=(car.x, car.y + 5), color='black', annotation_clip=False)

        fargs = [Fargs(
            ax=ax,
            sim=sim,
            path=path,
            car=car,
            car_outline=car_outline,
            front_right_wheel=front_right_wheel,
            front_left_wheel=front_left_wheel,
            rear_right_wheel=rear_right_wheel,
            rear_left_wheel=rear_left_wheel,
            rear_axle=rear_axle,
            annotation=annotation,
            target=target
        )]

        _ = FuncAnimation(fig, animate, frames=car.gen, init_func=lambda: None, fargs=fargs, interval=interval, repeat=sim.loop)
        # anim.save('animation.gif', writer='imagemagick', fps=50)
        
        plt.grid()
        plt.show()


    def calculate_error(self):
        while self.car.continue_animation:
            self.car.drive()
        
        return self.car.all_crosstrack_errors[0:-1]

