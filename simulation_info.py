# pylint: skip-file
from csv import reader
from dataclasses import dataclass
from math import radians

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from models.bicycle_model import BicycleModel
from libs import CarDescription, StanleyController, generate_cubic_spline
from models.model_factory import ModelFactory


class Simulation:

    def __init__(self, dt: float, max_size_x: int, max_size_y: int, frames: int, loop: bool = False):

        self.dt = dt
        self.map_size_x = max_size_x
        self.map_size_y = max_size_y
        self.frames = frames
        self.loop = loop


class Path:

    def __init__(self, file: str):

        # Get path to waypoints.csv
        with open(file, newline='') as f:
            rows = list(reader(f, delimiter=','))

        ds = 0.05

        time_temp, x_temp, y_temp, acceleration_temp = [[float(i) for i in row] for row in zip(*rows[1:])]
        non_duplicates = [i for i in range(1, len(x_temp)) if x_temp[i] != x_temp[i - 1]]
        
        x = [x_temp[i] for i in non_duplicates]
        y = [y_temp[i] for i in non_duplicates]
        
        time = [time_temp[i] for i in non_duplicates]
        self.delta_time = time[-1] / len(time)
        
        acceleration = [acceleration_temp[i] for i in non_duplicates]
        self.acceleration = acceleration

        self.px, self.py, self.pyaw, _ = generate_cubic_spline(x, y, ds)


class Car:

    def __init__(self, init_x, init_y, init_yaw, px, py, pyaw, acceleration, delta_time, vmax, model):

        # Model parameters
        self.x = init_x
        self.y = init_y
        self.yaw = init_yaw
        self.acceleration = acceleration
        self.delta_time = delta_time
        self.time = 0.0
        self.velocity = 0.0
        self.vmax = vmax
        self.wheel_angle = 0.0
        self.angular_velocity = 0.0
        max_steer = radians(31)
        wheelbase = 0.406

        # Tracker parameters
        self.px = px
        self.py = py
        self.pyaw = pyaw
        self.k = 8.0
        self.ksoft = 1.0
        self.kyaw = 0.01
        self.ksteer = 0.0
        self.crosstrack_error = None
        self.target_id = None
        self.iteration = 0

        # Description parameters
        self.colour = 'black'
        overall_length = 0.71
        overall_width = 0.30
        tyre_diameter = 0.107
        tyre_width = 0.053
        axle_track = 0.30 - 0.053
        rear_overhang = 0.5 * (overall_length - wheelbase)

        self.tracker = StanleyController(self.k, self.ksoft, self.kyaw, self.ksteer, max_steer, wheelbase, self.px, self.py, self.pyaw)
        self.model = ModelFactory(wheelbase, max_steer, self.delta_time).create_model(model)
        self.description = CarDescription(overall_length, overall_width, rear_overhang, tyre_diameter, tyre_width, axle_track, wheelbase)

    
    def get_acceleration(self, time):

        acceleration = self.acceleration[time]

        tol = 0.3
        if acceleration <= -tol:
            return acceleration * 9.82
        elif acceleration > -tol and acceleration < 0:
            return 0
        else:
            return acceleration * 9.82
    

    def plot_car(self):
        
        return self.description.plot_car(self.x, self.y, self.yaw, self.wheel_angle)


    def drive(self):
        
        acceleration = self.get_acceleration(self.iteration) if self.velocity < self.vmax else 0
        self.wheel_angle, self.target_id, self.crosstrack_error = self.tracker.stanley_control(self.x, self.y, self.yaw, self.velocity, self.wheel_angle)
        self.x, self.y, self.yaw, self.velocity, _, _ = self.model.update(self.x, self.y, self.yaw, self.velocity, acceleration, self.wheel_angle)
        self.iteration += 1

        print(f"Cross-track term: {self.crosstrack_error}{' '*10}", end="\r")


@dataclass
class Fargs:
    ax: plt.Axes
    sim: Simulation
    path: Path
    car: Car
    car_outline: plt.Line2D
    front_right_wheel: plt.Line2D
    front_left_wheel: plt.Line2D
    rear_right_wheel: plt.Line2D
    rear_left_wheel: plt.Line2D
    rear_axle: plt.Line2D
    annotation: plt.Annotation
    target: plt.Line2D
   

def animate(frame, fargs):

    ax                = fargs.ax
    sim               = fargs.sim
    path              = fargs.path
    car               = fargs.car
    car_outline       = fargs.car_outline
    front_right_wheel = fargs.front_right_wheel
    front_left_wheel  = fargs.front_left_wheel
    rear_right_wheel  = fargs.rear_right_wheel
    rear_left_wheel   = fargs.rear_left_wheel
    rear_axle         = fargs.rear_axle
    annotation        = fargs.annotation
    target            = fargs.target

    # Camera tracks car
    ax.set_xlim(car.x - sim.map_size_x, car.x + sim.map_size_x)
    ax.set_ylim(car.y - sim.map_size_y, car.y + sim.map_size_y)

    # Drive and draw car
    car.drive()
    outline_plot, fr_plot, rr_plot, fl_plot, rl_plot = car.plot_car()
    car_outline.set_data(*outline_plot)
    front_right_wheel.set_data(*fr_plot)
    rear_right_wheel.set_data(*rr_plot)
    front_left_wheel.set_data(*fl_plot)
    rear_left_wheel.set_data(*rl_plot)
    rear_axle.set_data(car.x, car.y)

    # Show car's target
    target.set_data(path.px[car.target_id], path.py[car.target_id])

    # Annotate car's coordinate above car
    annotation.set_text(f'{car.x:.1f}, {car.y:.1f}')
    annotation.set_position((car.x, car.y + 5))

    plt.title(f'{sim.dt*frame:.2f}s', loc='right')
    plt.xlabel(f'Speed: {car.velocity:.2f} m/s', loc='left')
    # plt.savefig(f'image/visualisation_{frame:03}.png', dpi=300)

    return car_outline, front_right_wheel, rear_right_wheel, front_left_wheel, rear_left_wheel, rear_axle, target,