from vehicle_simulation import VehicleSimulation

if __name__ == '__main__':

    data = "data/data4.csv"
    model = "BicycleModel"
    vmax = 3.75
    constant_velocity = False

    main = VehicleSimulation(data, model, vmax, constant_velocity)
    main.show_animation()
    main.calculate_error()