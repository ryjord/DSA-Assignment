# Customers
class Customer:
    def __init__(self, customer_id: int, demand: int):
        self.customer_id = customer_id
        self.demand = demand
        self.x_coordinate = 0.0
        self.y_coordinate = 0.0

# Vehicles
class Vehicle:
    def __init__(self, vehicle_id: int, max_capacity: int):
        self.vehicle_id = vehicle_id
        self.max_capacity = max_capacity
        self.current_load = 0

    # Demand check
    def can_carry(self, demand: int) -> bool:
        return (self.current_load + demand) <= self.max_capacity

    # Load demand
    def load(self, demand: int) -> None:
        if self.can_carry(demand):
            self.current_load += demand
        else:
            raise ValueError("Capacity exceeded for this vehicle.")


class VRPInstance:
    def __init__(self, customers: list, distance_matrix: list, vehicle_capacity: int, num_vehicles: int):
        self.customers = customers
        self.distance_matrix = distance_matrix
        self.vehicle_capacity = vehicle_capacity
        self.num_vehicles = num_vehicles
        # Exclude the depot from the overall customer count
        self.num_customers = len(customers) - 1

    @property
    def demands(self) -> list:
        return [customer.demand for customer in self.customers]