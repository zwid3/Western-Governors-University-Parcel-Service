import datetime

# Class to manage truck operations and tracking details.
class Truck:
    # Initialize truck attributes required for package delivery and route tracking.
    def __init__(self, number, packages, cur_time=datetime.time(hour=8), departure_time=datetime.time(hour=8),
                 speed=18.25, max_capacity=16, miles=0.0, cur_location='HUB'):
        self.number = number  # Unique truck identifier
        self.packages = packages  # List of package IDs assigned to the truck
        self.cur_time = cur_time  # Current time, tracking progress and end-of-day time
        self.departure_time = departure_time  # Time when the truck departs from the hub
        self.speed = speed  # Truck speed in miles per hour
        self.max_capacity = max_capacity  # Maximum number of packages the truck can carry
        self.miles = miles  # Total miles traveled
        self.cur_location = cur_location  # Truck's current location
