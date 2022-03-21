from math import sqrt
from read import demands, warehouses, drones, noflyzones, items, chargingstations, M, C
from read import Demand, Warehouse, Drone, NoFlyZone, Item, ChargingStation

deliveries = []


def possible(demand, drone):
    drone.set_capacity(drone.capacity+items[demand.Item-1].weight)
    drone.set_capacityvol(
        drone.capacityvol+items[demand.Item-1].L*items[demand.Item-1].B*items[demand.Item-1].H)
    drone.set_z(items[demand.Item-1].H)
    time_taken = time(drone.x, drone.y, drone.z,
                      demand.x, demand.y, demand.z,  drone.P*(drone.capacity/drone.fullcapacity), drone.Q*(drone.capacity/drone.fullcapacity))
    energy_consumed = battery_consumed(drone.ID, time_taken, 1)
    minimum = 1e18
    warehouseID = -1
    for warehouse in warehouses:
        if(time(demand.x, demand.y, demand.z, warehouse.x, warehouse.y, warehouse.z, drone.P*(drone.capacity/drone.fullcapacity), drone.Q*(drone.capacity/drone.fullcapacity)) < minimum):
            minimum = time(demand.x, demand.y, demand.z,
                           warehouse.x, warehouse.y, warehouse.z, drone.P*(drone.capacity/drone.fullcapacity), drone.Q*(drone.capacity/drone.fullcapacity))
            warehouseID = warehouse.ID
    energy_consumed += battery_consumed(drone.ID, minimum, 1)
    # print(time_taken+minimum, energy_consumed)
    if(energy_consumed <= drone.battery and drone.availabletime <= demand.startTime and drone.capacity <= drone.fullcapacity and drone.capacityvol <= drone.fullcapacityvol):
        drone.set_battery(drone.battery-energy_consumed)
        drone.set_capacity(drone.capacity-items[demand.Item-1].weight)
        drone.set_capacityvol(
            drone.capacityvol-items[demand.Item-1].L*items[demand.Item-1].B*items[demand.Item-1].H)
        drone.set_availabletime(time_taken+minimum +
                                time_to_charge(drone.ID, warehouseID))
        drone.set_used(1)
        drone.set_z(warehouses[warehouseID-1].z)
        drones[drone.ID-1].flighttime += time_taken+minimum
        drones[drone.ID-1].chargetime += time_to_charge(drone.ID, warehouseID)
        return True
    return False


def time(x1, y1, z1, x2, y2, z2, pf, qf):
    distancexy = (x2-x1)**2
    +(y2 - y1)**2
    distancez = abs(z2-z1)
    distancexy = sqrt(distancexy)
    time = distancexy/(M-pf)+distancez/(M-qf)+distancez/(M+qf)
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

drone_cnt = 0
total_cost = 0
for drone in drones:
    total_cost += drone.fixedcost+drone.variablecost * \
        (drone.flighttime/3600)+(drone.chargetime/3600)*C
    drone_cnt += drone.used
print(drone_cnt, total_cost)
