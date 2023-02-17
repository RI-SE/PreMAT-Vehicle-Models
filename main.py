from vehicle_simulation import VehicleSimulation
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def calculate_errors(dataList: list, models: list, vmax_range: list, constant_vel: bool = False) -> list:

    all_errors_mean = {}
    all_errors_std = {}

    for model in models:
        all_errors_mean[model] = {}
        all_errors_std[model] = {}
        for data in dataList:
            all_errors_mean[model][data] = {}
            all_errors_std[model][data] = {}
            for vmax in vmax_range:
                simulation = VehicleSimulation(data, model, vmax, constant_vel)
                errors = simulation.calculate_error()
                errors = [abs(i) for i in errors]
                all_errors_mean[model][data][vmax] = np.mean(errors)
                all_errors_std[model][data][vmax] = np.std(errors)
        
        print(model + " done!")
    
    return all_errors_mean, all_errors_std


def box_plot(data: dict, title: str):

    index = 0
    labels = []
    boxes = []
    info = []
    _, ax = plt.subplots()
    
    for outer_key in data.keys():
        colour = (float(np.random.rand(1)), float(np.random.rand(1)), float(np.random.rand(1)))
        info.append((outer_key, colour))
        for inner_key in data[outer_key].keys():
            box = ax.boxplot(data[outer_key][inner_key].values(), positions = [index], patch_artist=True)
            boxes.append((box, colour))
            index += 1
            labels.append(inner_key)
    
    ax.set_xticklabels(labels, rotation = 15)
    for box, colour in boxes:
        for patch in box['boxes']:
            patch.set_facecolor(colour)
            

    legend = []
    for name, colour in info:
        legend.append(mpatches.Patch(color = colour, label = name))


    ax.set_ylabel("[m]")
    ax.legend(handles = legend, loc = "upper left")
    ax.set_title(title)


if __name__ == '__main__':

    data = ["data1.csv", "data3.csv", "data5.csv"]
    models = ["BicycleModel", "DubinsCar"]
    vmax_range = np.linspace(3, 4, 8).tolist()

    mean_values, std_values = calculate_errors(data, models, vmax_range, True)
    box_plot(mean_values, "Mean values, with acceleration")
    box_plot(std_values, "Standard deviations, with acceleration")
    
    mean_values, std_values = calculate_errors(data, models, vmax_range, False)
    box_plot(mean_values, "Mean values, constant velocity")
    box_plot(std_values, "Standard deviations, constant velocity")
    

    plt.show()

    # For showing an animation of a simulation
    # sim = VehicleSimulation("data/data5.csv", "DubinsCar", 3.75, True)
    # sim.show_animation()


    