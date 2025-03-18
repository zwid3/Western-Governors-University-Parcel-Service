#Brian Ndlovu
#010399627
#Revised WGUPS Project Task 2
#02/23/2025

import csv
from datetime import time
import DirectHashTable
import Package
from Truck import Truck
from load_trucks import load_trucks
from deliver_packages import deliver_packages
from interface import interface


# Load data from CSV files into appropriate data structures.

# Read addresses from CSV and store them in a list.
with open('csv/address.csv') as csv_address:
    address_list = csv.reader(csv_address)
    address_list = list(address_list)

# Read distance data from CSV and store it in a list.
with open('csv/distance.csv') as csv_distance:
    distance_list = csv.reader(csv_distance)
    distance_list = list(distance_list)

# Initialize a hash table to store package data.
package_table = DirectHashTable.DirectHashTable()

# Read package details from CSV and insert them into the hash table.
with open('csv/package.csv') as csv_package:
    package_csv = csv.reader(csv_package)
    for row in package_csv:
        temp_package = Package.Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        package_table.insert(int(row[0]), temp_package)

# Initialize three trucks, assigning unique numbers.
# Truck 3 has a delayed start time of 9:05 AM due to delayed packages.
truck1 = Truck(1, [])
truck2 = Truck(2, [])
truck3 = Truck(3, [], time(hour=9, minute=5), time(hour=9, minute=5))

# Create a hash table to store truck data.
trucks = DirectHashTable.DirectHashTable(3)
trucks.insert(truck1.number, truck1)
trucks.insert(truck2.number, truck2)
trucks.insert(truck3.number, truck3)


# Load packages onto trucks and execute delivery operations.
load_trucks(package_table, trucks, address_list, distance_list, truck1, truck2, truck3)
deliver_packages(package_table, trucks, address_list, distance_list, truck1, truck2, truck3)

# Launch the user interface for package tracking and truck status updates.
interface(package_table, trucks)
