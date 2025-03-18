from datetime import time
from Truck import Truck
from DirectHashTable import DirectHashTable


# Iterates through package data and prints relevant details.
# This function is used in multiple parts of the interface to avoid redundancy.
def interface_loop(package_table, trucks, check_time):
    truck1_packages = []
    truck2_packages = []
    truck3_packages = []
    delivered = []
    column_names = f'\033[1mPackage ID | {"Address":<67} | Weight | Truck | Deadline | Status\033[0m'

    for i in range(1, 41):
        cur_package = package_table.search(i)
        if cur_package.delivery_time is not None and cur_package.delivery_time < check_time:
            delivered.append(cur_package.id)
        elif cur_package.truck == 1:
            truck1_packages.append(cur_package.id)
        elif cur_package.truck == 2:
            truck2_packages.append(cur_package.id)
        else:
            truck3_packages.append(cur_package.id)

    print()
    print('Delivered items:')
    print(column_names)
    for package_id in delivered:
        cur_package = package_table.search(package_id)
        cur_package.lookup(check_time, trucks)

    truck_packages = (truck1_packages, truck2_packages, truck3_packages)
    for i in range(len(truck_packages)):
        truck_number = i + 1
        cur_truck_packages = truck_packages[i]
        truck = trucks.search(truck_number)
        if cur_truck_packages:
            print()
            print(f'Packages on truck {truck_number}:')
            print(column_names)
            for package_id in cur_truck_packages:
                cur_package = package_table.search(package_id)
                cur_package.lookup(check_time, trucks)


# Provides an interactive menu for retrieving package and delivery information.
# Continues running until the user selects option 4 to exit.
def interface(package_table: DirectHashTable, trucks: DirectHashTable):
    # Retrieve truck objects to calculate total miles for menu option 1.
    truck1: Truck = trucks.search(1)
    truck2: Truck = trucks.search(2)
    truck3: Truck = trucks.search(3)

    # Reusable menu text to keep the interface concise.
    menu_text = ('--------\n'
                 '1. Print all packages and total miles\n'
                 '2. Get a single package with a time\n'
                 '3. Get all packages with a time\n'
                 '4. Exit\n'
                 '--------\n')

    menu_input = '0'
    # Loops until the user selects option 4 to exit.
    while menu_input != '4':
        menu_input = input(menu_text).strip()
        if menu_input == '4':
            break
        # Validates user input to ensure a correct menu selection.
        elif menu_input not in {'1', '2', '3'}:
            print('Please choose a valid option')
            continue

        # 1. Display all packages and total miles.
        elif menu_input == '1':
            print(f'Total miles: {format(truck1.miles + truck2.miles + truck3.miles, ".1f")}')
            # Uses 23:00 to retrieve all deliveries completed throughout the day.
            check_time = time(hour=23)
            interface_loop(package_table, trucks, check_time)
            print()
            continue

        # 2. Retrieve a single package's status at a specified time.
        elif menu_input == '2':
            package_input = input('Enter a package ID between 1 and 40 to check: ')
            package_id = -1
            check_time = time(hour=0)

            # Ensures the input is a valid package ID.
            while True:
                try:
                    package_id = int(package_input)
                except ValueError:
                    package_input = input('Invalid package ID (1-40). Please enter a valid ID: ')
                    continue
                if package_id < 1 or package_id > 40:
                    package_input = input('Invalid package ID (1-40). Please enter a valid ID: ')
                    continue
                else:
                    break

            time_input = input('Enter a time to check (HH:MM): ')

            # Ensures the input is a valid time format.
            while True:
                try:
                    temp_time = time_input.split(':')
                    check_time = time(hour=int(temp_time[0]), minute=int(temp_time[1]))
                except ValueError:
                    time_input = input('Invalid time format (HH:MM). Please enter a valid time: ')
                    continue
                break

            package = package_table.search(package_id)
            print()
            print(f'\033[1mPackage ID | {'Address':<67} | Weight | Truck | Deadline | Status\033[0m')
            package.lookup(check_time, trucks)
            print()

        # 3. Retrieve all packages' statuses at a specified time.
        elif menu_input == '3':
            time_input = input('Enter a time to check (HH:MM): ')
            check_time = time(hour=0)

            # Ensures the input is a valid time format.
            while True:
                try:
                    temp_time = time_input.split(':')
                    check_time = time(hour=int(temp_time[0]), minute=int(temp_time[1]))
                except ValueError:
                    time_input = input('Invalid time format (HH:MM). Please enter a valid time: ')
                    continue
                break

            interface_loop(package_table, trucks, check_time)
            print()
