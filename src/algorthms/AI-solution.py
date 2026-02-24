import pydash as _;
def run_ai_solution(distance_matrix, demands, vehicle_capacity):
  num_locations = len(distance_matrix);
  unvisited = set(range(1, num_locations));
  routes = [];
  total_dist = 0;
  while unvisited:
    curr_route = [0];
    curr_cap = vehicle_capacity;
    curr_loc = 0;
    while unvisited:
      best_next = None;
      min_dist = float('inf');
      for customer in unvisited:
        if demands[customer] <= curr_cap and distance_matrix[curr_loc][customer] < min_dist:
          best_next = customer;
          min_dist = distance_matrix[curr_loc][customer];
      if _.is_none(best_next):
        break;
      curr_route.append(best_next);
      unvisited.remove(best_next);
      curr_cap -= demands[best_next];
      total_dist += min_dist;
      curr_loc = best_next;
    total_dist += distance_matrix[curr_loc][0];
    curr_route.append(0);
    routes.append(curr_route);
  return { 'routes': routes, 'total_distance': total_dist };