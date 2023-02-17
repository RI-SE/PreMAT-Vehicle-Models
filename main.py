from vehicle_simulation import VehicleSimulation


def calculate_errors(dataList: list, models: list, vmax: float) -> list:
    for model in models:
        for data in dataList:
            print("Data: " + data)
            print("Model: " + model)
            simulation = VehicleSimulation(data, model, vmax, True)
            simulation.calculate_error()
            print("")    
    

if __name__ == '__main__':

    data = ["data/data1.csv", "data/data3.csv", "data/data5.csv"]
    models = ["BicycleModel", "DubinsCar"]
    vmax = 3.75
    calculate_errors(data, models, vmax)

    # a = VehicleSimulation("data/data5.csv", "DubinsCar", 3.75, True)
    # a.show_animation()


    