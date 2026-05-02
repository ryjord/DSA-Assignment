# Customers
class Customer:
    def __init__(self, customer_id: int, demand: int):
        # Init customer id, demand, x coordinate, y coordinate
        self.customer_id = customer_id
        self.demand = demand
        self.x_coordinate = 0.0
        self.y_coordinate = 0.0

# Vehicles
class Vehicle:
    def __init__(self, vehicle_id: int, max_capacity: int):
        # Init vehicle id, max capacity, current load
        self.vehicle_id = vehicle_id
        self.max_capacity = max_capacity
        self.current_load = 0

    # Demand check
    def can_carry(self, demand: int) -> bool:
        # Return true if capacity allows
        return (self.current_load + demand) <= self.max_capacity

    # Load demand
    def load(self, demand: int) -> None:
        # Add demand if capacity allows
        if self.can_carry(demand):
            self.current_load += demand
        else:
            raise ValueError("Capacity exceeded for this vehicle.")


# Instance / Problem Description
class VRPInstance:
    def __init__(self, customers: list, distance_matrix: list, vehicle_capacity: int, num_vehicles: int):
        # Init customers, matrix, capacity, num_vehicles
        self.customers = customers
        self.distance_matrix = distance_matrix
        self.vehicle_capacity = vehicle_capacity
        self.num_vehicles = num_vehicles
        # Exclude the depot from the overall customer count
        self.num_customers = len(customers) - 1

    # Demands list
    @property
    def demands(self) -> list:
        return [customer.demand for customer in self.customers]