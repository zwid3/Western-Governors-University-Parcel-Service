from datetime import time
from DirectHashTable import DirectHashTable

class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, note='', truck=-1, delivery_time=None):
        self.id = id  # Unique package identifier
        self.address = address  # Delivery address
        self.city = city  # Destination city
        self.state = state  # Destination state
        self.zip = zip  # Postal code
        self.deadline = deadline  # Required delivery deadline
        self.weight = weight  # Package weight (kg)
        self.note = note  # Special delivery instructions
        self.truck = truck  # Assigned truck number (-1 if not assigned)
        self.delivery_time = delivery_time  # Timestamp of delivery

    def __str__(self):
        full_address = f'{self.address}, {self.city}, {self.state}, {self.zip}'
        return (f'{self.id:>10} | {full_address:<67} | '
                f'{self.weight:>3}kgs | {self.truck:>5} | {self.deadline:<8}')

    def lookup(self, check_time: time, trucks: DirectHashTable):
        truck: Truck = trucks.search(self.truck)
        if self.delivery_time is not None and self.delivery_time < check_time:
            formatted_time = self.delivery_time.strftime('%H:%M:%S')
            print(f'{self} | Delivered at {formatted_time}')

        elif truck.departure_time > check_time:
            print(f'{self} | At the hub')
        else:
            # Handle package #9 address correction logic
            if self.id == 9:
                incorrect_address = '300 State St' # Storing the incorrect address
                correct_address = '410 S State St' # Storing the correct address

                if check_time < time(hour=10, minute=20):
                    # Display the incorrect address before 10:20 AM
                    full_address = f'{incorrect_address}, {self.city}, {self.state}, {self.zip}'
                    print(f'{self.id:>10} | {full_address:<67} | '
                          f'{self.weight:>3}kgs | {self.truck:>5} | {self.deadline:<8} | En Route')
                else:
                    # Display the correct address after 10:20 AM
                    self.address = correct_address # Setting the correct address
                    full_address = f'{self.address}, {self.city}, {self.state}, {self.zip}'
                    print(f'{self.id:>10} | {full_address:<67} | '
                          f'{self.weight:>3}kgs | {self.truck:>5} | {self.deadline:<8} | En Route')
            else:
                # Display other packages
                print(f'{self} | En Route')
