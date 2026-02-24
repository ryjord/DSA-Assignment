
class Customer:
  def __init__(self, id, demand, x=0, y=0):
    self.id = id;
    self.demand = demand;
    self.x = x;
    self.y = y;


class Vehicle:
  def __init__(self, id, capacity):
    self.id = id;
    self.capacity = capacity;
    self.current_load = 0;


class Route:
  def __init__(self, depot_id=0):
    self.nodes = [depot_id];
    self.total_demand = 0;

  def add_customer(self, customer):
    self.nodes.append(customer.id);
    self.total_demand += customer.demand;