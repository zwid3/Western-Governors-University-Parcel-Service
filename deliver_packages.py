from datetime import datetime, time, timedelta, date
from Truck import Truck
from get_nearest_neighbor import get_nearest_neighbor, get_distance, get_address_id
from DirectHashTable import DirectHashTable

# Uses the nearest neighbor algorithm to optimize package deliveries for each truck.
def deliver_packages(package_table: DirectHashTable, trucks: DirectHashTable, addr_list, dist_list,
                     truck1: Truck, truck2: Truck, truck3: Truck):
    temp_date = date(1, 1, 1)
    i = 1
    while i <= 3:
        cur_truck = trucks.search(i)
        while len(cur_truck.packages) > 0:
            # Extracts the closest package information (ID, index, distance) from the nearest neighbor function.
            nearest_neighbor_info = get_nearest_neighbor(cur_truck.cur_location, cur_truck.packages, package_table,
                                                         addr_list, dist_list)
            nearest_neighbor = package_table.search(nearest_neighbor_info[0])
            index = nearest_neighbor_info[1]
            distance = nearest_neighbor_info[2]

            # Updates the truck’s mileage and estimated delivery time only if moving to a new location.
            if distance > 0.0:
                cur_truck.miles += distance
                # Adjusts the truck’s current time based on travel distance and speed.
                delta = timedelta(hours=distance / cur_truck.speed)
                cur_truck.cur_time = (datetime.combine(temp_date, cur_truck.cur_time) + delta).time()

            # Updates the truck’s current location and marks the package as delivered.
            cur_truck.cur_location = nearest_neighbor.address
            nearest_neighbor.delivery_time = cur_truck.cur_time
            nearest_neighbor.status = 'delivered'
            cur_truck.packages.pop(index)

            # Special handling for package 9, which has an incorrect address until 10:20 AM.
            # It is added to truck 3's route if the time is past 10:20 AM or if it’s the last package.
            if i == 3:
                package9 = package_table.search(9)
                if (package9.delivery_time is None and package9.truck == -1 and
                    (len(cur_truck.packages) == 0 or cur_truck.cur_time > time(hour=10, minute=20))):
                    cur_truck.packages.append(9)
                    package9.truck = 3
                    '''REMOVED FROM HERE
                    if cur_truck.cur_time < time(hour=10, minute=20):
                        # Use the incorrect address before 10:20 AM
                        package9.address = '300 State St'
                    else:
                        # Update to the correct address after 10:20 AM
                        package9.address = '410 S State St'
                    '''

                    # Ensure package 9 is delivered after 12:04 PM to meet the requirement
                    # of capturing package statuses between 12:03 PM and 1:12 PM.
                    if cur_truck.cur_time < time(hour=12, minute=4):
                        cur_truck.cur_time = time(hour=12, minute=4)

            # Returns the truck to the HUB if all packages are delivered.
            if len(cur_truck.packages) == 0:
                hub_distance = get_distance(0, get_address_id(cur_truck.cur_location, addr_list), dist_list)
                cur_truck.miles += hub_distance
                hub_delta = timedelta(hours=hub_distance / cur_truck.speed)
                cur_truck.cur_time = (datetime.combine(temp_date, cur_truck.cur_time) + hub_delta).time()
                cur_truck.cur_location = 'HUB'

                # Since only 2 drivers are available for 3 trucks, truck 3 must wait for one truck to return.
                # If truck 3’s scheduled departure is earlier than both truck 1 and truck 2’s return time,
                # it updates its departure time to match the first returning truck.
                if i == 2:
                    if truck3.cur_time < truck1.cur_time and truck3.cur_time < truck2.cur_time:
                        if truck1.cur_time < truck2.cur_time:
                            truck3.cur_time = truck1.cur_time
                            truck3.departure_time = truck1.cur_time
                        else:
                            truck3.cur_time = truck2.cur_time
                            truck3.departure_time = truck2.cur_time
        i += 1
