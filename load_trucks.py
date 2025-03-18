from DirectHashTable import DirectHashTable
from get_nearest_neighbor import get_nearest_neighbor
from Truck import Truck


# Loads trucks by first assigning packages with special conditions, then adding packages with the same address
# as already assigned ones, and finally distributing the remaining packages based on proximity.
def load_trucks(package_table: DirectHashTable, trucks: DirectHashTable, address_list, distance_list,
                truck1: Truck, truck2: Truck, truck3: Truck):
    # Separate packages with special conditions and temporarily store the rest.
    remaining_packages = []
    for package in package_table.table:
        cur_package = package[1]
        note = str(cur_package.note)
        if cur_package is None:
            continue
        # Group packages 13, 15, and 19 along with those requiring joint delivery.
        elif ((cur_package.id == 13 or cur_package.id == 15 or cur_package.id == 19)
              or (note in ['Must be delivered with 15, 19', 'Must be delivered with 13, 19', 'Must be delivered with 13, 15'])):
            truck2.packages.append(cur_package.id)
            cur_package.truck = 2
            continue
        # Assign packages restricted to truck 2.
        elif note == 'Can only be on truck 2':
            truck2.packages.append(cur_package.id)
            cur_package.truck = 2
            continue
        # Assign packages with delays to truck 3.
        elif note in ['Delayed on flight---will not arrive to depot until 9:05 am', 'Wrong address listed']:
            truck3.packages.append(cur_package.id)
            cur_package.truck = 3
            continue
        # Prioritize early deadline packages for truck 1 (express truck).
        elif cur_package.deadline in ['10:30 AM', '9:00 AM']:
            truck1.packages.append(cur_package.id)
            cur_package.truck = 1
            continue
        # Store all other packages for later distribution.
        else:
            remaining_packages.append(cur_package.id)
            continue

    # Add remaining packages that share an address with already assigned ones.
    for truck in trucks.table:
        cur_truck = truck[1]
        cur_package_list = cur_truck.packages
        i = 0
        if len(cur_package_list) > 0:  # Skip empty trucks
            while i < len(cur_package_list):
                distance = 0.0
                cur_package = package_table.search(cur_package_list[i])
                # Find and assign packages with the same address.
                while distance == 0.0:
                    nearest_neighbor_info = get_nearest_neighbor(cur_package.address, remaining_packages, package_table,
                                                                 address_list, distance_list)
                    nearest_neighbor = package_table.search(nearest_neighbor_info[0])
                    index = nearest_neighbor_info[1]
                    distance = nearest_neighbor_info[2]
                    if distance == 0.0:
                        cur_truck.packages.append(nearest_neighbor.id)
                        remaining_packages.pop(index)
                        nearest_neighbor.truck = cur_truck.number
                i += 1

    # Distribute remaining packages, starting from truck 2.
    k = 2
    while k <= 3:
        cur_truck = trucks.search(k)
        # Get the last package assigned to the truck or start from none.
        cur_package = package_table.search(cur_truck.packages[-1]) if cur_truck.packages else None

        while len(cur_truck.packages) < cur_truck.max_capacity and remaining_packages:
            # Start from the hub if the truck is empty; otherwise, use the last package's address.
            nearest_neighbor_info = get_nearest_neighbor('HUB' if not cur_truck.packages else cur_package.address,
                                                         remaining_packages, package_table, address_list, distance_list)
            nearest_neighbor = package_table.search(nearest_neighbor_info[0])
            index = nearest_neighbor_info[1]
            # Assign the package to the truck and remove it from the remaining list.
            cur_truck.packages.append(nearest_neighbor.id)
            remaining_packages.pop(index)
            cur_package = nearest_neighbor
            cur_package.truck = k

        # Temporarily remove package 9 due to an incorrect address; it will be reassigned later.
        if k == 3:
            cur_truck.packages.remove(9)
            package_table.search(9).truck = -1
        k += 1
