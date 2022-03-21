import pandas as pd
data = pd.read_csv('Demand.csv')
M = 0
C = 0
demands = []
drones = []
warehouses = []
items = []


def filter(row):
    ID = int(row['Type'][-1])
    value = int(row['Value'])
    obj = None
    if(row['Type'].startswith('Drone')):
        obj = Drone(ID)
    elif(row['Type'].startswith('WH')):
        obj = Warehouse(ID)
        obj.set_iswarehouse(1)

    if(row['Parameter_ID'][0] == 'P'):
        obj.set_P(value)
    elif(row['Parameter_ID'][0] == 'Q'):
        obj.set_Q(value)
    elif(row['Parameter_ID'][0] == 'A'):
        obj.set_A(value)
    elif(row['Parameter_ID'][0] == 'B'):
        obj.set_B(value)
    elif(row['Parameter_ID'][0] == 'C'):
        obj.set_C(value)
    elif(row['Parameter_ID'].startswith('DT')):
        obj.set_cnt(value)
    if(row['Type'].startswith('Drone')):
        drones.append(obj)
    elif(row['Type'].startswith('WH')):
        warehouses.append(obj)


class Item:
    def __init__(self, ID, weight, L, B, H):
        self.ID = ID
        self.weight = weight
        self.L = L
        self.B = B
        self.H = H

    def set_weight(self, weight):
        self.weight = weight

    def set_L(self, L):
        self.L = L

    def set_B(self, B):
        self.B = B

    def set_H(self, H):
        self.H = H

    def __str__(self):
        summary = []
        str1 = ' '
        summary.append(str(self.ID))
        summary.append(str(self.weight))
        summary.append(str(self.L))
        summary.append(str(self.B))
        summary.append(str(self.H))
        return str1.join(summary)


class Demand:
    def __init__(self, ID, ItemID, WarehouseID, Day, x, y, z, startTime, endTime, fail):
        self.ID = ID
        self.Day = Day
        self.Item = ItemID
        self.WarehouseID = WarehouseID
        self.x = x
        self.y = y
        self.z = z
        self.startTime = startTime
        self.endTime = endTime
        self.fail = fail

    def __str__(self):
        summary = []
        str1 = ' '
        summary.append(str(self.ID))
        summary.append(str(self.Day))
        summary.append(str(self.Item))
        summary.append(str(self.WarehouseID))
        summary.append(str(self.x))
        summary.append(str(self.y))
        summary.append(str(self.z))
        summary.append(self.startTime)
        summary.append(self.endTime)
        summary.append(str(self.fail))
        return str1.join(summary)


class Warehouse:

    def __init__(self, ID):
        self.ID = ID
        self.x = 0
        self.y = 0
        self.z = 0
        self.current = 0
        self.is_warehouse = 0
        self.slots = 0

    def set_iswarehouse(self, val):
        self.is_warehouse = val

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_z(self, z):
        self.z = z

    def set_slots(self, slots):
        self.slots = slots

    def set_current(self, current):
        self.slots = current

    def __str__(self):
        summary = []
        str1 = ' '
        summary.append(str(self.ID))
        summary.append(str(self.x))
        summary.append(str(self.y))
        summary.append(str(self.z))
        return str1.join(summary)


class Drone:
    def __init__(self, ID):
        self.ID = ID
        self.A = 0.0
        self.B = 0.0
        self.C = 0.0
        self.P = 0.0
        self.Q = 0.0
        self.cnt = 0
        self.weight = 0
        self.slots = 0
        self.fullslots = 0
        self.battery = 0
        self.fullbattery = 0
        self.capacity = 0
        self.fullcapacity = 0
        self.capacityvol = 0
        self.fullcapacityvol = 0

    def set_A(self, A):
        self.A = A

    def set_B(self, B):
        self.B = B

    def set_C(self, C):
        self.C = C

    def set_P(self, P):
        self.P = P

    def set_Q(self, Q):
        self.Q = Q

    def set_cnt(self, cnt):
        self.cnt = cnt

    def set_fullbattery(self, fullbattery):
        self.fullbattery = fullbattery

    def set_battery(self, battery):
        self.battery = battery

    def set_fullslots(self, fullslots):
        self.fullslots = fullslots

    def set_slots(self, slots):
        self.slots = slots

    def set_weight(self, weight):
        self.weight = weight

    def set_capacity(self, capacity):
        self.capacity = capacity

    def set_fullcapacity(self, fullcapacity):
        self.fullcapacity = fullcapacity

    def set_fullcapacityvol(self, fullcapacityvol):
        self.fullcapacityvol = fullcapacityvol

    def set_capacityvol(self, capacityvol):
        self.capacityvol = capacityvol

    def __str__(self):
        summary = []
        str1 = ' '
        summary.append(str(self.ID))
        summary.append(str(self.A))
        summary.append(str(self.B))
        summary.append(str(self.C))
        summary.append(str(self.P))
        summary.append(str(self.Q))
        summary.append(str(self.cnt))
        return(str1.join(summary))


for index, row in data.iterrows():
    ID = int(row['Demand ID'][1:])
    ItemID = int(row['Item'][5:])
    WarehouseID = int(row['WH'][2:])
    Day = int(row['Day'][4:])
    x = int(row['X'])
    y = int(row['Y'])
    z = int(row['Z'])
    startTime = row['DeliveryFrom']
    endTime = row['DeliveryTo']
    fail = int(row['DeliveryFailure'])
    demands.append(Demand(ID, ItemID, WarehouseID, Day,
                   x, y, z, startTime, endTime, fail))


data = pd.read_csv('Parameters.csv')
for index, row in data.iterrows():
    if(index == 0):
        M = row['Value']
    elif(index == 1):
        C = row['Value']
    else:
        filter(row)

data = pd.read_csv('Items.csv')
for index, row in data.iterrows():
    ID = int(row['Item Id'][-1])
    weight = int(row['Weight (KG)'])
    L = int(row['Length'])/100
    B = int(row['Breadth'])/100
    H = int(row['Height'])/100
    items.append(Item(ID, weight, L, B, H))

data = pd.read_csv('Drones.csv')

for index, row in data.iterrows():
    ID = int(row['Drone Type'][-1])
    print(row['Battery Capacity'])
