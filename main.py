from simulation_info import Simulation, Car, Path, Fargs, animate
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np

class Main:
    def __init__(self):
        self.path = Path("data/data5.csv")
        self.sim  = Simulation(self.path.delta_time, max_size_x = 5, max_size_y = 5, frames = len(self.path.acceleration))
        self.car  = Car(self.path.px[0], self.path.py[0], self.path.pyaw[0],
                        self.path.px, self.path.py, self.path.pyaw, self.path.acceleration,
                        self.path.delta_time, 3.64, "BicycleModel")


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
        
        print("")
        print(f"Sum, all cross-track terms: {sum(self.car.all_crosstrack_errors[0:-1])}")
        print(f"Mean, all cross-track terms: {np.mean(self.car.all_crosstrack_errors[0:-1])}")
        print(f"Standard deviation, all cross-track terms: {np.std(self.car.all_crosstrack_errors[0:-1])}")


if __name__ == '__main__':
    main = Main()
    # main.show_animation()
    main.calculate_error()