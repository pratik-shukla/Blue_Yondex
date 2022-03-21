from math import sqrt
from read import demands, warehouses, drones, noflyzones, items, chargingstations, M, C
from read import Demand, Warehouse, Drone, NoFlyZone, Item, ChargingStation

deliveries = []


def possible(demand, drone):
    time_taken = time(drone.x, drone.y, drone.z, demand.x, demand.y, demand.z)
    drone.set_capacity(drone.capacity+items[demand.Item-1].weight)
    energy_consumed = battery_consumed(drone.ID, time_taken, 1)
    minimum = 1e18
    warehouseID = -1
    for warehouse in warehouses:
        if(time(demand.x, demand.y, demand.z, warehouse.x, warehouse.y, warehouse.z) < minimum):
            minimum = time(demand.x, demand.y, demand.z,
                           warehouse.x, warehouse.y, warehouse.z)
            warehouseID = warehouse.ID
    energy_consumed += battery_consumed(drone.ID, minimum, 1)
    # print(time_taken+minimum, energy_consumed)
    if(energy_consumed <= drone.battery and drone.availabletime <= demand.startTime and drone.capacity <= drone.fullcapacity):
        drone.set_battery(drone.battery-energy_consumed)
        drone.set_capacity(0)
        drone.set_availabletime(time_taken+minimum +
                                time_to_charge(drone.ID, warehouseID))
        drone.set_used(1)
        return True
    return False


def time(x1, y1, z1, x2, y2, z2):
    distance = (x2-x1)**2
    +(y2 - y1)**2
    +(z2-z1)**2
    distance = sqrt(distance)
    time = distance/M
    return time


def time_to_charge(droneID, warehouseID):
    droneID -= 1
    warehouseID -= 1
    charge_needed = drones[droneID].fullbattery-drones[droneID].battery
    time = (charge_needed/(warehouses[warehouseID].current*1000))*3600
    return time


def battery_consumed(droneID, time, is_ascending):
    droneID -= 1
    total_weight = drones[droneID].weight+drones[droneID].capacity
    multiplier = drones[droneID].A+drones[droneID].B * \
        M+(drones[droneID].z*is_ascending)
    energy = total_weight*multiplier
    return energy


for demand in demands:
    for drone in drones:
        if(possible(demand, drone)):
            print("Demand->", demand.ID, "Drone->", drone.ID)
            break


for delivery in deliveries:
    print(delivery)
count = 0
for drone in drones:
    count += drone.used
print(count)
