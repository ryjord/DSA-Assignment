import json;
import pydash as _;
def load_test_case(filepath):
  try:
    with open(filepath, 'r') as file:
      data = json.load(file);
      return data;
  except Exception as error:
    print(f"Error loading file: { error }");
    return None;
def calculate_route_distance(route_nodes, distance_matrix):
  if _.is_empty(route_nodes):
    return 0;
  distance = 0;
  for i in range(len(route_nodes) - 1):
    distance += distance_matrix[route_nodes[i]][route_nodes[i+1]];
  return distance;